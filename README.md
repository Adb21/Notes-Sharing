# Note Sharing App 

## Featues :
- CRUD operation of Note by authenticated User
- Sharing of Note by authenticated User
- Login and Registration

## Techstack :
- API Framework : DRF  (*Choose DRF due to ease of setup wih inbuilt serializers, ORM and Testing functionalities over FastAPI*) 
- Database : SQLite3 (Default) or MySQL
- Authentication : JWT
- Rate Limiting : 500/day for authenticated User Scope
- Testing Lib : DRF's inbuilt - APITestCase
- API Docs : Swagger UI

## Steps to run Localy :
 - Setup virtual env (**python3 -m venv venv**)
 - Install pip requirenemtns (**pip install -r requirnemets.txt**)
 - add .env (check env variables from .env.example)
 - Default Database is SQLite3 on env varaible **DATABASE_CHOICE=DEFAULT**
 - If want to use MySQL, then change DATABASE_CHOICE=MySQL and set DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT in env
 - If you’re on Linux, chances are you might run into some error while trying to install mysqlclient : sudo apt install python3-dev libmysqlclient-dev
 - To migrate base tables run command : **python3 manage.py migrate**
 - To run server : **python3 manage.py runserver**
 - server will start on http://127.0.0.1:8000 and swagger UI is at same link
 - To run Tests : **python3 manage.py test**

## API Summary:

| API                   | Type    | Description          |  Body |
| ----------------------|:-------:| --------------------:|------:|
| api/auth/signup       | POST    | User Registration    | username, first_name, last_name, email, password |
| api/auth/login        | POST    | User Login           | username, password |
| api/notes/            | POST    | Create Note          | title, content |
| api/notes/            | GET     | Get list of Note     | |
| api/notes/<:id>        | GET    | Reterive Note by id  | |
| api/notes/<:id>        | PUT     | Update Note by id    | title, content |
| api/notes/<:id>        | DELETE  | Delete Note by id    | |
| api/notes/<:id>/share  | GET     | Reterive Sharable id for note from response | |
| api/notes?uid=<sharable_id>  | GET     | Reterive Shared note from another user using Sharable id| |
| api/notes?search=<:keyword>  | GET     | Search Notes based on Keywords| |




