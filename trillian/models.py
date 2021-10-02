from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from django.db import models
import grpc
import crypto.keyspb.keyspb_pb2
import trillian_admin_api_pb2_grpc
import trillian_admin_api_pb2
import trillian_log_api_pb2_grpc
import trillian_log_api_pb2
from google.protobuf import duration_pb2
import jwt
import logging
import json
import hashlib
import time
from datetime import datetime
from accounts.models import Profile


# Create your models here.
class SingletonModel(models.Model):

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class SingleInstanceMetaClass(type):
    def __init__(self, name, bases, dic):
        self.__single_instance = None
        super().__init__(name, bases, dic)


PK_USER2 = """-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAzY9lFVAQjjENAoenxC6v
Q2zhG9DSq6FC0+MuYOr6ko7lf+yRhnG33kPoO/OoESvWmxAutsKzhW/PdvVAYQxz
SzhVFFC69kvYbVff7ex00fJDdTIU6NgpV3CKy6clP4hqqbdagSttELUhXjcbalu0
uHrgfyiL20h/vjQwe/YYscVAv15IxK5Ky+wJ4lLY6JPUNgrkGZ3rgHROivBmwTc4
j+lP0T+x12oC254YovxGMR14ITgq6q2Whbdvg1TZXL81wLL7WseWtSYJt14NUA8U
SzAoJbxr1/UpAymnSa6BLxZRkj8rTIafMtj4aZVmDfzgkAk8IlOyj4HbYyTZRZk3
sAKh5ptrnNvMuw4WL/ZWLpHo5ZDNW9FVpsDhaXZL8fmJ1dUPyJ7sTf4qw2AFgVBb
MLfv72m2kExZ5nFT+Ugp/geNOifed6Ti1cwwboTsFLjejaH59qEzbgy3B3nxUGq5
iS2xhGBHBrgLJl502scpzLSLxt3DTL/CotNYGN4uIipvWkVDYJV4m9jxnMvvOeVW
GVk2R8WyINqkjFC3puETDO0pseWtU5jqDY5bzfvdiWfMDsGK/e8A1YudvAvyFD8k
3/kEsChNX+ojM28hDS1WDnpwiCaBY5Vyj09xMmLGbKuLDit+onfxG306pQF+PCOQ
Vr8ZWvmfUSEr6QHgBJUdTdsCAwEAAQ==
-----END PUBLIC KEY-----"""


class Trillian(metaclass=SingleInstanceMetaClass):
    def __init__(self, key_algorithm=['ES256', 'RS256']):
        '''Initialize the trillian personality with its key pair,
        the allowed algorithms and the dictionaries of the resource
        servers and clients that are added to the Merkle Tree. Start
        also the services to communicate with the Trillian server'''
        key_pair = Trillian.generate_key()
        self.sk = key_pair[0].private_bytes(encoding=serialization.Encoding.PEM,
                                            format=serialization.PrivateFormat.PKCS8,
                                            encryption_algorithm=serialization.
                                            BestAvailableEncryption(password=b'password2'))

        self.pk = key_pair[1].public_bytes(encoding=serialization.Encoding.PEM,
                                           format=serialization.PublicFormat.
                                           SubjectPublicKeyInfo)
        self.allowed_algorithms = key_algorithm
        #PK_USER2 = Profile.objects.get(user__username='user2').public_key
        #self.allowed_servers = {'user2': PK_USER2}
        self.allowed_servers = {}
        self.server = {}
        self.clients = {}
        # Open the connection with the Trillian server and the service to use the API
        channel = grpc.insecure_channel('localhost:8090')
        self.stub = trillian_admin_api_pb2_grpc.TrillianAdminStub(channel)
        self.stub2 = trillian_log_api_pb2_grpc.TrillianLogStub(channel)
        # Create the three and initialize it
        self.tree_id = self.create_tree()
        self.init_log(self.tree_id)
        self.tree_size = 0

    def __call__(self):
        return self

    @classmethod
    def generate_key(cls):
        sk = ec.generate_private_key(curve=ec.SECP256R1())
        pk = sk.public_key()
        return sk, pk

    def create_tree(self):
        '''Create the tree'''
        max_root_duration = duration_pb2.Duration(seconds=3600)
        response = self.stub.CreateTree(
            trillian_admin_api_pb2.CreateTreeRequest(tree={"tree_state": 'ACTIVE',
                                                           "tree_type": 'LOG',
                                                           "hash_strategy": 'RFC6962_SHA256',
                                                           "hash_algorithm": 'SHA256',
                                                           "signature_algorithm": 'ECDSA',
                                                           "display_name": '',
                                                           "description": '',
                                                           "max_root_duration": max_root_duration},
                                                     key_spec=crypto.keyspb.keyspb_pb2.
                                                     Specification(
                                                         ecdsa_params={"curve": 'P256'})))
        return response.tree_id

    def init_log(self, tree_id):
        '''Log to initialize the tree'''
        response = self.stub2.InitLog(trillian_log_api_pb2.
                                      InitLogRequest(log_id=tree_id,
                                                     charge_to=trillian_log_api_pb2.
                                                     ChargeTo(user='test')))
        return response

    def queue_leaf(self, tree_id, leaf_value, leaf_identity_hash, extra_data=''):
        '''Insert a leaf in the tree'''
        response = self.stub2.QueueLeaf(
            trillian_log_api_pb2.
                QueueLeafRequest(log_id=tree_id,
                                 leaf={'leaf_value': f'{leaf_value}'.encode(),
                                       'extra_data': f'{extra_data}'.encode(),
                                       'leaf_identity_hash': leaf_identity_hash}))
        return response

    def inclusion_proof(self, tree_id, leaf_id, tree_size):
        '''Return the inclusion proof for a leaf, indicated with his id,
        for a specific size of the tree'''
        try:
            response = self.stub2.GetInclusionProof(
                trillian_log_api_pb2.GetInclusionProofRequest(log_id=tree_id,
                                                              leaf_index=leaf_id,
                                                              tree_size=tree_size))
            return response
        except grpc._channel._InactiveRpcError:
            return None

    def inclusion_proof_by_hash(self, tree_id, merkle_leaf_hash, tree_size):
        '''Return the inclusion proof for a leaf, indicated with his hash,
        for a specific size of the tree'''
        # m = hashlib.sha256()
        # m.update(f'\0{leaf_value}'.encode())
        # leaf_hash = bytes.fromhex(m.digest().hex())
        try:
            response = self.stub2.GetInclusionProofByHash(
                trillian_log_api_pb2.GetInclusionProofByHashRequest(log_id=tree_id,
                                                                    leaf_hash=merkle_leaf_hash,
                                                                    tree_size=tree_size))
            return response
        except grpc._channel._InactiveRpcError:
            return None

    def update_info(self, data, leaf_index):
        '''Update the dictionary of clients and servers that are added
        to the log'''
        if data["server"] in self.server.keys():
            self.server[data["server"]].append([data["client"], leaf_index,
                                                data["nbf"], data["exp"]])
        else:
            self.server[data["server"]] = [[data["client"], leaf_index,
                                            data["nbf"], data["exp"]]]
        if data["client"] in self.clients.keys():
            self.clients[data["client"]].append([data["server"], leaf_index,
                                                 data["nbf"], data["exp"]])
        else:
            self.clients[data["client"]] = [[data["server"], leaf_index,
                                             data["nbf"], data["exp"]]]

    def decode_jwt(self, token, authorization_server_pk):
        '''Decode a JWT'''
        try:
            data = jwt.decode(jwt=token, key=authorization_server_pk,
                              algorithms=self.allowed_algorithms,
                              options={"require_exp": True, "verify_exp": True,
                                       # "verify_iss":True,
                                       "require_nbf": True,
                                       "verify_signature": True})
        except jwt.exceptions.ExpiredSignatureError as e:
            print("The token has expired")
            logging.exception(e)
            raise ValueError("Expired Token") from e
        except jwt.exceptions.ImmatureSignatureError as e:
            print("The validity of the token has not started")
            logging.exception(e)
            raise ValueError("Immature Token") from e
        except jwt.exceptions.InvalidSignatureError as e:
            print("The signature does not match the one "
                  "provided as part of the token")
            logging.exception(e)
            raise ValueError("Invalid signature") from e
        except jwt.exceptions.DecodeError as e:
            print("Token cannot be decoded because it failed validation")
            logging.exception(e)
            raise ValueError("Failed validation") from e
        except jwt.exceptions.InvalidTokenError as e:
            print("Invalid token")
            logging.exception(e)
            raise ValueError("Invalid Token") from e
        if data["iss"] not in self.allowed_servers.keys() or \
                self.allowed_servers[data["iss"]] != \
                authorization_server_pk:
            print(type(self.allowed_servers[data["iss"]]))
            print(type(authorization_server_pk))
            print("Invalid issuer")
            raise ValueError("Invalid Issuer")
        #        except jwt.exceptions.InvalidIssuerError:
        #            print("Invalid issuer")
        #            return
        return data

    def insert_jwt(self, data,  token, authorization_server_pk):
        # data = self.decode_jwt(token, authorization_server_pk)
        # print(data)
        if data is not None:
            leaf_value = json.dumps({'client': data["client"],
                                     'server': data["server"], 'id': data["id"],
                                     'exp': data["exp"], 'nbf': data["nbf"]},
                                    sort_keys=True)
            leaf_identity = f"{data['client']} {data['server']} {data['id']}"
            m = hashlib.sha256()
            m.update(f'{leaf_identity}'.encode())
            leaf_identity_hash = m.digest()
            print(f'Leaf value: {leaf_value}')
            leaf_added = self.queue_leaf(self.tree_id, leaf_value, leaf_identity_hash)
            print(f'Leaf added:\n{leaf_added}')
            # time.sleep(1)     #Waiting to be sure that the leaf has been added
            # inclusion = leaf_added.queued_leaf.leaf.leaf_index
            merkle_leaf_hash = leaf_added.queued_leaf.leaf.merkle_leaf_hash
            status_code = leaf_added.queued_leaf.status.code
            if status_code == 0:
                self.tree_size += 1
                for _ in range(1000):
                    time.sleep(0.2)
                    inclusion_proof = self.inclusion_proof_by_hash(self.tree_id,
                                                                   merkle_leaf_hash,
                                                                   self.tree_size)
                    if inclusion_proof is not None:
                        break
                else:
                    raise RuntimeError("Trillian timeout")
                print(f'Inclusion Proof:\n{inclusion_proof}')
                leaf_index = inclusion_proof.proof[0].leaf_index
                self.update_info(data, leaf_index)
            elif status_code == 6:
                print("Leaf already present in the log")
                inclusion_proof = self.verify_inclusion(data["client"],
                                                        data["server"],
                                                        datetime.utcnow().isoformat())
            elif status_code == 9:
                print("The operation was rejected because the system is not "
                      "in a state required for the operation's execution")
            elif status_code == 3:
                print("The client specified an invalid argument")
            return inclusion_proof, status_code

    def client_connected_to_server(self, server):
        '''Check if a server is in the log and, if it is, print clients
        that are allowed to access it'''
        try:
            return self.server[f"{server}"]
        except KeyError as e:
            print("The server is not present in the log")
            logging.exception(e)
            raise KeyError("The server is not present in the log") from e

    def server_connected_to_client(self, client):
        '''Check if a client is in the log and, if it is, print servers
        that he has permission to access'''
        try:
            return self.clients[f"{client}"]
        except KeyError as e:
            print("The client is not present in the log")
            logging.exception(e)
            raise KeyError("The client is not present in the log") from e

    def verify_inclusion(self, client, resource_server, time):
        server_connected = self.server_connected_to_client(client)
        # [server, id, start_validity, expiration_time]
        servers = [server for server in server_connected
                   if server[0] == resource_server]
        for server in servers:
            if datetime.utcfromtimestamp(int(server[3])) >= datetime.fromisoformat(time) >= \
                    datetime.utcfromtimestamp(int(server[2])):
                leaf_id = server[1]
                inclusion_proof = self.inclusion_proof(self.tree_id, leaf_id,
                                                       self.tree_size)
                print(f"Inclusion proof:\n"
                      f"{inclusion_proof}")
                return inclusion_proof
        print("The client is not allowed in the server")
        return None



