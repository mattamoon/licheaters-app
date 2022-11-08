# licheaters-app

# Install
1. Clone the repo
2. Install requirements.txt  


## Check for cheaters:
1. Open app.py
2. Update with your user details, # of games and dates
3. Add your api key to the .env file to speed up searches

```
    lichess_obj.user = 'YourUsernameHere'  # set user to check games for
    lichess_obj.max_games = 10  # set max amount of games to review
    lichess_obj.start = '2022/1/1'  # from YYYY/m/d format
    lichess_obj.end = '2022/12/31'  # to YYYY/m/d format 
    
