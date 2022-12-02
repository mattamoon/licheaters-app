import os
from gathercheater.gathercheater import GatherCheater
from gathercheater.functions import *
from gathercheater.constants import *
from flask import Flask, jsonify, url_for, render_template, redirect, session, request, flash
from authlib.integrations.flask_client import OAuth
from requests.exceptions import HTTPError
import requests

# Environment Variables
load_dotenv()

# Constants
LICHESS_HOST = os.getenv("LICHESS_HOST", "https://lichess.org")

# Flask Config
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config['LICHESS_CLIENT_ID'] = os.getenv("LICHESS_CLIENT_ID")
app.config['LICHESS_AUTHORIZE_URL'] = f"{LICHESS_HOST}/oauth"
app.config['LICHESS_ACCESS_TOKEN_URL'] = f"{LICHESS_HOST}/api/token"

# Oauth Config
oauth = OAuth(app)
oauth.register('lichess', client_kwargs={"code_challenge_method": "S256"})


# Licheater App Functions
def check_user_details():
    # using the gathercheater package to create GatherCheater object
    lichess_obj = GatherCheater()

    # Set user details
    lichess_obj.user = 'basilcandle'  # set user to check games for
    lichess_obj.max_games = 10  # set max amount of games to review
    lichess_obj.start = '2022/1/1'  # from YYYY/m/d format
    lichess_obj.end = '2022/12/31'  # to YYYY/m/d format

    return lichess_obj


def licheater_data():
    licheater = check_user_details()
    games = licheater.games_by_player_dates(game_dates(licheater.start), game_dates(licheater.end))
    players_from_games = licheater.get_players_from_games(games)
    player_list = list_util(players_from_games, licheater.user)
    player_dfs = players_to_df(player_list)
    total_iterations = len(player_dfs)
    while licheater.df_index <= total_iterations:
        try:
            player_dfs[licheater.df_index]
        except(IndexError,):
            print('Data Analysis Complete! \n')
            break
        else:
            player_list = create_player_list(player_dfs[licheater.df_index])
            data_string = create_player_string(player_list)
            data = licheater.games_by_player_list(data_string)
            licheater.data_list.extend(data)
            licheater.df_index += 1

    return licheater.data_list


# script to get accounts


# licheater_data = licheater_data()
# tos_accounts, closed_accounts, good_accounts = GatherCheater.check_cheaters(licheater_data)


@app.route('/login')
def login():
    redirect_uri = url_for("authorize", _external=True)
    return oauth.lichess.authorize_redirect(redirect_uri)


@app.route('/authorize', methods=['GET'])
def authorize():
    token = oauth.lichess.authorize_access_token()
    bearer = token['access_token']
    headers = {'Authorization': f'Bearer {bearer}'}
    response = requests.get(f"{LICHESS_HOST}/api/account", headers=headers, timeout=10)
    response.raise_for_status()
    if response.status_code == 200:
        profile = response.json()
        session['user'] = profile['id']
        return redirect(url_for('home'))
    else:
        return f'404'


# Flask routing to display accounts using Jinja templates
@app.route('/', methods=['POST', 'GET'])
def home():
    if 'user' in session:
        return render_template('authenticated.html', user=session['user'])
    else:
        return render_template('index.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    # flash('You have been logged out!', 'info')
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
