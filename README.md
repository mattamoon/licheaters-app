# licheaters-app

Check if you played against anyone on Lichess now marked as violating ToS or if they closed their account. 

# Install
1. Clone Repo
2. ```pip install -r requirements.txt```


# Create api access token on Lichess
1. https://lichess.org/account/oauth/token
    - Read & Write preferences checked under 'User Account'
2. Copy & paste this value in your .env file where 'api_key={Insert token here - remove brackets}' (paste after the = sign - no quotes needed)

# Create a secret key
1. You can do this by creating a new python file:
```
import secrets

print(secrets.token_hex())
```

Run this and then copy & paste this value in your .env file where 'SECRET_KEY=" "' (paste value after = sign, in between the quotes)

# Run app.py
- Navigate to http://127.0.0.1:5000 or http://localhost:5000/
- Enter your username or login through lichess ( login will greatly speed up the search)
- Enter an appropriate date range
- Enter # of games to check
- Click Analyze Games and then have some patience! :-)

# Notes/Info:
- Lichess ToS: ```https://lichess.org/terms-of-service```
- If someone violated the ToS and then closed their account, they will show as Closed.


