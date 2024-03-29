from flask import Flask, url_for, render_template, redirect, session, request, flash
from gathercheater.gathercheater import GatherCheater, berserk
from gathercheater.functions import *
from gathercheater.constants import *
from authlib.integrations.flask_client import OAuth
from authlib.integrations.base_client.errors import OAuthError
from requests.exceptions import HTTPError
import os
import requests
import datetime as dt

# Environment Variables
load_dotenv()

# Constants
LICHESS_HOST = os.getenv("LICHESS_HOST", "https://lichess.org")
LICHESS_TOKEN = os.getenv("api_key")

# Flask Config
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config['LICHESS_CLIENT_ID'] = os.getenv("LICHESS_CLIENT_ID")
app.config['LICHESS_AUTHORIZE_URL'] = f"{LICHESS_HOST}/oauth"
app.config['LICHESS_ACCESS_TOKEN_URL'] = f"{LICHESS_HOST}/api/token"

# Oauth Config
oauth = OAuth(app)
oauth.register('lichess', client_kwargs={"code_challenge_method": "S256"})


@app.route('/login')
def login():
    redirect_uri = url_for("authorize", _external=True)
    return oauth.lichess.authorize_redirect(redirect_uri)


@app.route('/authorize', methods=['GET'])
def authorize():
    try:
        token = oauth.lichess.authorize_access_token()
    except OAuthError:
        flash('User login cancelled! Please try again or enter your username above!', 'info')
        return redirect(url_for('home'))
    bearer = token['access_token']
    headers = {'Authorization': f'Bearer {bearer}'}
    response = requests.get(f"{LICHESS_HOST}/api/account", headers=headers, timeout=10)
    response.raise_for_status()
    if response.status_code == 200:
        profile = response.json()
        session['user'] = profile['id']
        session['token'] = bearer
        return redirect(url_for('home'))
    else:
        return f'404'


@app.route('/', methods=['POST', 'GET'])
def home():
    if 'user' in session:
        if request.method == 'POST':
            # Get form values
            session['dfrom'] = request.form['df']  # date from
            session['dto'] = request.form['dt']  # date to
            session['mg'] = request.form['mg']  # max games
            return redirect(url_for('analyze'))
        else:
            return render_template('authenticated.html', user=session['user'])
    else:
        if request.method == 'POST':
            session['form_user'] = request.form['liuser']
            session['dfrom'] = request.form['df']  # date from
            session['dto'] = request.form['dt']  # date to
            session['mg'] = request.form['mg']  # max games
            return redirect(url_for('analyze'))
        else:
            return render_template('index.html')


@app.route('/analyze', methods=['POST', 'GET'])
def analyze():
    # Establish Client with Token if available
    if LICHESS_TOKEN:
        auth_token = berserk.TokenSession(LICHESS_TOKEN)
        licheater = GatherCheater()
        licheater.lichess = berserk.Client(auth_token)
    else:
        licheater = GatherCheater()
    # Set Variables
    if 'user' in session:
        licheater.user = session['user']
    else:
        licheater.user = session['form_user']
    new_start = session['dfrom']
    new_end = session['dto']
    if new_start > new_end:
        flash('Date Range not valid!')
        redirect(url_for('home'))
    else:
        licheater.start = new_start
        licheater.end = new_end
    if int(session['mg']) > 0:
        licheater.max_games = int(session['mg'])
    else:
        flash('Max Games must be > 0', 'info')
        return redirect(url_for('home'))
    # Get Game Data
    try:
        games = licheater.games_by_player_dates()
        players_from_games = licheater.get_players_from_games(games)
    except berserk.exceptions.ResponseError:
        flash('User not found!', 'info')
        return redirect(url_for('home'))
    except OSError:
        flash('Date Error - Try again!')
        return redirect(url_for('home'))
    else:
        player_list = list_util(players_from_games, licheater.user)
        player_dfs = players_to_df(player_list)
        total_iterations = len(player_dfs)
        while licheater.df_index <= total_iterations:
            try:
                player_dfs[licheater.df_index]
            except(IndexError,):
                break
            else:
                player_list = create_player_list(player_dfs[licheater.df_index])
                data_string = create_player_string(player_list)
                data = licheater.games_by_player_list(data_string)
                licheater.data_list.extend(data)
                licheater.df_index += 1

        tos_accounts, closed_accounts, good_accounts = GatherCheater.check_cheaters(licheater.data_list)

    return render_template('analysis.html', tos=tos_accounts, closed=closed_accounts, good=good_accounts)


@app.route('/logout')
def logout():
    session.pop('token', None)
    session.pop('user', None)
    flash('You have been logged out!', 'info')
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
