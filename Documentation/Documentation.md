# Apalucha web

## Settings

- Config example:

```json
{
    "setuped": false,
    "database": {
        "address": "db",
        "port": 3306,
        "username": "Funni",
        "password": "WhoNeedSecurePasswordAnywayAmIRight?",
        "name": "apalucha",
        "poolSize": 40,
        "poolOverflow": 25,
        "poolRecycle": 3600,
        "poolTimeout": 35,
        "tableNames": {
            "admin": "Admins",
            "user": "Users",
            "default": "Films"
        }
    },
    "jwt": {
        "secret": "LeSecrete",
        "expiration": 7,
        "issuer": "https://apalucha.kaktusgame.eu",
        "algorithm": "HS256"
    },
    "pdfs": {
        "path": "./pdfs/",
        "template": "template.pdf",
        "loginUrl": "https://apalucha.kaktusgame.eu/login",
        "pdfUrl": "https://apalucha.kaktusgame.eu/pdf"
    },
    "voting": {
        "voteDuration": 20,
        "voteInProgress": false,
        "voteEnd": null
    },
    "flask": {
        "address": "0.0.0.0",
        "port": 5000,
        "debug": false,
        "masterUsername": "LeMaster",
        "masterPassword": "Passworde123"
    }
}
```

## Backend

### Backend logging

__apalucha_logging.py__:
    - **class CustomFormatter(logging.Formatter)** -> Custom formatter for logging (like colors, ...)
    - **DailyFileHandler(logging.FileHandler)** -> Custom file handler for logging (creates new log file every day)
    - **CustomRequestHandler(WSGIRequestHandler)** -> Custom request handler for flask (overwrites default log handler)
    - **apalucha_logger** -> Logger for backend, logs to console and file via function log
    - **log(level, message)** -> Logs message with level to console and file

### AUTH

- Stuff used for authentication (JWT, password hashing, etc.)

- __Login.py__:
    - **createadmin("username", "password", session)** -> Creates admin user in database
    - **login("username", "password", session)** -> Checks if admin user exists in database and returns JWT token if password is correct
- __tokens.py__:
    - **load_config()** -> Loads config, checks if secret is set if not it generates one
    - **generate_jwt(secret, expiration, issuer, algorithm, user_id, is_admin=False)** -> Generates JWT token
    - **decode_jwt(token, secret, issuer, algorithm)** -> Decodes JWT token

### Management

- Used by /admin API endpoint, to manage users and films

- __film_mng.py__:
    - **add_film("title", "title", "team", "session")** -> Adds film to database
    - **remove_film("film_id", "session")** -> Removes film from database
- __user_mng.py__:
    - **add_user(session, isAdmin=False, username=None, password=None, pdfs_settings=None, jwt_settings=None)** -> If isAdmin is True, it creates admin user, else it creates normal user. In case of normal user, it also creates pdfs which has QR codes for user to login with token
    - **remove_user(session, user_id, isAdmin=False)** -> Removes user from database
- __qr_codes.py__:
    - **generate_qr_code(url)** -> Generates QR code for user to login with token
- __pdfs_generator.py__:
    - **generate_pdf(url, template_filename, new_filename)** -> Generates PDF with QR code for user to login with token based on template

### PDFs

- Directory with PDFs for users to login with token, also contains template for PDFs


### SQL

- Handles SQL connections and queries

- __sql_config.py__:
    - **make_engine(database)** -> Creates engine for SQL connection
- __sql_init.py__:
    - Has functions for creating tables in database if they don't exist

#### SQL_Syntax

- Contains sql files for creating tables 

### Voting

- Handles voting for films

- __voting.py__:
    - **vote_film(film_id, user_id, session)** -> Adds vote for film to database
- __film_ranking.py__:
    - **count_votes(session)** -> Counts votes for films and sets their final vote count
    - **unsorted_films(session)** -> Returns films before voting (for starting voting)
    - **sorted_films(session)** -> Returns films after voting (for ending voting)





# Backend API Endpoints

- API endpoints for backend

## /management

```json
{
    "action": "<action>",
    "data": {
        <data>
    }
}
```

### remove_film

```json
{
    "action": "remove_film",
    "data": {
        "film_id": "<film_id>"
    }
}
```

### add_film

```json
{
    "action": "add_film",
    "data": {
        "title": "<title>",
        "team": "<team>"
    }
}
```

### remove_user

```json
{
    "action": "remove_user",
    "data":{
        "isAdmin": True/False,
        "user_id": "<user_id>"
    }
}
```

### add_user

```json
{
    "action": "add_user",
    "data":{
        "isAdmin": True/False,
        "username": "<username>",
        "password": "<password>"
    }
}
```

### reset
    
```json
{
    "action": "reset",
    "data": {
        "reset_secret": True/False,
        "full_reset": True/False
    }
}
```

## /pdf

- URL -> /pdf?user=<user_id>
- Method -> GET
- Returns PDF with QR code for user to login with token

## /login

- URL -> /login
- Method -> POST
- Returns JWT token if username and password are correct

```json
{
    "username": "<username>",
    "password": "<password>"
}
```

## /voting

- URL -> /voting
- Method -> GET, POST
- Returns unsorted films for voting (GET), sends vote for film (POST)

```json
{
    "vote": "<film_id>"
}
```

## /scoreboard

- URL -> /scoreboard
- Method -> POST
- First POST starts voting, while end of voting is in future server will return unsorted films + time left, when voting ends server will return sorted films

First POST, server will return:
```json
{
    "voteEnd": "<time>",
    "voteDuration": "<time>",
    "films": {
            "1": "Film 1",
            "2": "Film 2"
        }
}
```

When voting is in progress, server will return:
```json
{
    "voteEnd": "<time>",
    "voteDuration": "<remaining_time>",
    "films":{
            "1": "Film 1",
            "2": "Film 2"
        }
}
```

When voting ends, server will return:
```json
{
    "voteEnd": false,
    "films":{
            "1": "Film 2",
            "2": "Film 1"
        },
    "votes":[1, 2]
}
```
