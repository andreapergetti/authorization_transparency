# authorization transparency

## Configuration
Clone the repository
```
git clone -b personality https://github.com/andreapergetti/authorization_transparency
```
Move in the directory <br>
```
cd authorization_transparency
```
Create virtual environment and install package required in the Pipfile
```
pipenv install
```
Start virtual environment
```
pipenv shell
```
To fix some problem with the [protobuf binary](https://github.com/protocolbuffers/protobuf/issues/2739):
```
pipenv uninstall protobuf
export PIP_NO_BINARY=protobuf && pipenv install protobuf
```

### Trillian personality
Create a Docker Volume to persist the database:
```
docker volume create trillian-data
```
Run an instance of MySQL using Docker:
```
docker run \
--name=database \
--env=MYSQL_ALLOW_EMPTY_PASSWORD=yes \
--mount=source=trillian-data,target=/var/lib/mysql \
--publish=3306:3306 mariadb:10.4
```
Run a script to reset the database and set up the expected tables:
```
./scripts/resetdb.sh
```

For simple deployments, running in a container is an easy way to get up and running with a local database. To use Docker to run and interact with the personality, use:
```
docker-compose --compatibility -f docker-compose.yml up -d
```
The option --compatibility is use to limit the amount of CPU, set in the docker-compose file, that containers can use.

If you want to have a web interface for the database managment of Trillian you can browse:
```
http://localhost:8080/
```

### Web application
Run Django server
```
python manage.py runserver
```
Open browser in localhost
```
http://127.0.0.1:8000
```

## How it works
### Create token to release authorization
First you have to log in or register in the web application and set the public key. Then you can create a token using the corresponding private key:
```
import jwt
from cryptography.hazmat.primitives import serialization
with open('jwtRS256.key', 'rb') as f:
	key=serialization.load_pem_private_key(f.read(), password=None)
token = jwt.encode(payload={'iss':'user2', 'client':'Lilo', 'server':'Finn', 'id':'0', 'exp':'1642882541', 'nbf':'1632882541'}, key=key, algorithm='RS256')
```
The field used in the encoding function are:
- 'iss': username of the server that create token
- 'client': name of the client
- 'server': name of the resource server
- 'id': identifier that user can use to enumerate his granted permission. This value is not stored in the system so the user has to take care of it, if he wants to use it. We suggest to use an incremental value.
- 'exp': expiration time of authorization. You can pass this value as a UTC UNIX timestamp (an int) or as a datetime
- 'nbf': time before which the authorization must not be accepted for processing. You can pass this value as a UTC UNIX timestamp (an int) or as a datetime

In the repository we provide a key pair that you can use to test this API. The public key(*jwtRS256.key.pub* file) is already set as the public key of *user2* in the database that we provide. The corrisponding private key is in the file *jwtRS256.key*.

User credentials in the database provided are:
- username: *user2* &nbsp;&nbsp; password: *utente222*
- username: *user1* &nbsp;&nbsp; password: *utente11*
## Examples of using the API REST
### Authorization List:<br>
List all authorizations
```
curl '127.0.0.1:8000/api/v1/authorizations'
```
Filter authorizations for server
```
curl '127.0.0.1:8000/api/v1/authorizations?server=Kronk'
```
Filter authorizations for client
```
curl '127.0.0.1:8000/api/v1/authorizations?client=Yzma'
```
Filter authorizations for server and client
```
curl '127.0.0.1:8000/api/v1/authorizations?server=Kronk&client=Yzma'
```

### Authorization create:
Create authorization with *user1* as user and the information set in the payload
```
curl -u user1 -X POST http://127.0.0.1:8000/api/v1/authorizations/create -H "Content-Type: application/json" -d '{"server":"server1", "client":"client1", "start_validity":"2021-07-29T20:00", "expiration_time":"2021-08-18T20:00"}'
```

### Authorization update:
Retrieve information to check current information about the authorization you want to update
```
curl -u user1 -X GET http://127.0.0.1:8000/api/v1/authorizations/41/update
```
If you want to do only partial update use PATCH method
```
curl -u user1 -X PATCH http://127.0.0.1:8000/api/v1/authorizations/create -H "Content-Type: application/json" -d '{"server":"server1", "client":"client1", "start_validity":"2021-07-29T20:00", "expiration_time":"2021-08-18T20:00"}'
```
If you want change the resource in his entirely use PUT method
```
curl -u user1 -X PUT http://127.0.0.1:8000/api/v1/authorizations/create -H "Content-Type: application/json" -d '{"server":"new_server", "client":"new_client", "start_validity":"2021-08-29T20:00", "expiration_time":"2021-09-18T20:00"}'
```

### Authorization delete:
Retrieve information to check current information
```
curl -u user1 -X GET http://127.0.0.1:8000/api/v1/authorizations/41/delete
```
Delete the authorization
```
curl -u user1 -X DELETE http://127.0.0.1:8000/api/v1/authorizations/41/delete
```

### Authorization create with JWT:
Step to create a token from a file called *jwtRS256.key*
```
import jwt
from cryptography.hazmat.primitives import serialization
with open('jwtRS256.key', 'rb') as f:
	key=serialization.load_pem_private_key(f.read(), password=None)
token = jwt.encode(payload={'client':'cc', 'server':'ss', 'exp':'2021-08-17', 'nbf':'2021-07-17'}, key=key, algorithm='RS256')
```

Create the authorization(*TOKEN* is the string obtained in the previous step)
```
curl -X POST http://127.0.0.1:8000/api/v1/authorizations/jwt/create/ -H "Content-Type: application/json" -d '{"user":"user2", "token":"TOKEN"}
```
