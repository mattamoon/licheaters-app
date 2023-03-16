from flask import Flask, url_for, render_template, redirect, session, request, flash
from gathercheater.gathercheater import GatherCheater
from gathercheater.functions import *
from gathercheater.constants import *
from authlib.integrations.flask_client import OAuth
from authlib.integrations.base_client.errors import OAuthError
from requests.exceptions import HTTPError
import os
import requests
import datetime as dt

# Load environment variables
load_dotenv()

# Constant
LICHESS_HOST = os.getenv("LICHESS_HOST", "https://lichess.org")

# Flask Config
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ('SECRET_KEY')
app.config['LICHESS_CLIENT_ID'] = os.environ('LICHESS_CLIENT_ID')
app.config['LICHESS_AUTHORIZE_URL'] = f"{LICHESS_HOST}/oauth"
app.config['LICHESS_ACCESS_TOKEN_URL'] = f"{LICHESS_HOST}/api/token"

# Oauth Config
oauth = OAuth(app)
oauth.register('lichess', client_kwargs={"code_challenge_method": "S256"})


# Licheater helper function
def date_fmt(dt_obj):
    str_date_fmt = '%Y-%m-%d'
    dt_date_fmt = '%Y/%m/%d'
    dto = dt.datetime.strptime(dt_obj, str_date_fmt)
    dt_str = dto.strftime(dt_date_fmt)
    return dt_str


def session_user():
    if 'user' in session:
        return session['user']
    else:
        return session['form_user']


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
    # Create GatherCheater Object
    licheater = GatherCheater()
    # Create Client Session
    if 'token' in session:
        b_session = berserk.TokenSession(session['token'])
        licheater.lichess = berserk.Client(b_session)
    else:
        licheater.lichess = berserk.Client()
    # Set User
    licheater.user = session_user()
    # Get Date Values
    new_start = date_fmt(session['dfrom'])
    new_end = date_fmt(session['dto'])
    # Check Dates for issues
    if new_start > new_end:
        flash('Date Range not valid!')
        redirect(url_for('home'))
    else:
        licheater.start = new_start
        licheater.end = new_end
    # Get Max Games value
    if int(session['mg']) > 0:
        licheater.max_games = int(session['mg'])
    else:
        flash('Max Games must be > 0', 'info')
        return redirect(url_for('home'))

    # Get Game Data
    try:
        games = licheater.games_by_player_dates(game_dates(licheater.start), game_dates(licheater.end))
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


if __name__ == '__main__':
    app.run(debug=False)
