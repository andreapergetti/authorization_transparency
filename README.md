# authorization transparency

## What is authorization transparency?
This project aim to create a Web application that allows some Authorization Server to release to Clients access grant for some Server in a transparent and verifiable manner. In this way everybody can check and observe Authorization Server's behaviour to identify who acts maliciously or release wrong authorization. In order to achieve the transparency of this process a [verifiable data structure](https://www.continusec.com/static/VerifiableDataStructures.pdf) is used to store authorization information. The particular data structure used is [Trillian](https://github.com/google/trillian).

## Using the code
Clone the repository
```
git clone https://github.com/andreapergetti/authorization_transparency
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
Run Django server
```
python manage.py runserver
```
Open browser in localhost
```
http://127.0.0.1:8000
```

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

In the repository we provide a key pair that you can use to test this API. The public key(*jwtRS256.key.pub* file) is already set as the public key of *user2* in the database that we provide.
