# licheaters-app

Search if you played against anyone on Lichess now marked as violating ToS or if they closed their account. 

# Install Options:
### 1. Clone Repo & Install Requirements
- Setup venv and run ```pip install -r requirements.txt```
### 2. Compose with Docker
- ```docker-compose up -d```
# Setup
#### 1. Create a Secret Key for Flask in the .env file.
```
import secrets

print(secrets.token_hex())
```
#### 2. Optional - Create an api access token on Lichess & Copy the value to the .env file
- https://lichess.org/account/oauth/token (Read & Write preferences under 'User Account')
# RUN app.py or compose with docker
- Navigate to http://127.0.0.1:5000

# Notes/Info:
- Lichess ToS: ```https://lichess.org/terms-of-service```
- If someone violated the ToS and then closed their account, they will show as Closed.

# TBD:
- Link to the game(s) played
- Filter by game type

# Thanks!
- lakinwecker for [lichess-oauth-flask example](https://github.com/lakinwecker/lichess-oauth-flask)



