# licheaters-app

Check if you played against anyone on Lichess now marked as violating ToS or if they closed their account. 

# Install
1. Fork the repo or download the zip with files!
2. Install requirements.txt  


## Check for cheaters!:
1. Open app.py
2. Update with your user details, # of games and dates
3. Add your api key to the .env file to speed up searches (optional but recommended)

```
    Setup your Lichess user details in app.py:
    
    lichess_obj.user = 'YourUsernameHere'  # set user to check games for
    lichess_obj.max_games = 10  # set max amount of games to review
    lichess_obj.start = '2022/1/1'  # from YYYY/m/d format
    lichess_obj.end = '2022/12/31'  # to YYYY/m/d format 
```

## Run app.py
    
## Review the data!    
    
    
```
    Output Example:
    
    Violated Lichess ToS: ['rekhawagh']
    Total violated: 1 

    Closed accounts: [] 
    Total closed: 0 

    Good Status...for now: ['batosz91', 'carlo2010', 'Charlie-J-Reilly', 'clopes2020', 'DavidHRivas17', 'didnotseethatm', 'elias_26', 'Enzo_12chess', 'geraldo_oliveira68', 'goodwin28', 'GregB65', 'heymeow69', 'Hritik_952003', 'JessicaCardiel', 'Jusva76', 'mansoor999', 'MaximT2', 'Osoflores', 'rylannovember', 'Sempreavanti61', 'SerbianSea', 'soulhunter03', 'Zhenye'] 
    Total good: 23

    Total user accounts reviewed: 24
```
    
