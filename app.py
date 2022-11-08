from gathercheater.gathercheater import GatherCheater
from gathercheater.functions import *
from gathercheater.constants import *


def check_user_details():
    # checks for API Key in the .env file -- greatly speeds up the searches!
    # add .env to your gitignore
    configure()

    # using the gathercheater package to create GatherCheater object
    lichess_obj = GatherCheater()

    # Set user details
    lichess_obj.user = 'basilcandle'  # set user to check games for
    lichess_obj.max_games = 10  # set max amount of games to review
    lichess_obj.start = '2022/1/1'  # from YYYY/m/d format
    lichess_obj.end = '2022/12/31'  # to YYYY/m/d format

    return lichess_obj


def app(licheater):
    games = licheater.games_by_player_dates(game_dates(licheater.start), game_dates(licheater.end))
    players_from_games = licheater.get_players_from_games(games)
    player_list = list_util(players_from_games, licheater.user)
    player_dfs = players_to_df(player_list)
    total_iterations = len(player_dfs)
    # Loop through list of dataframes
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

    lichess.display_data(lichess.data_list)


if __name__ == "__main__":
    lichess = check_user_details()
    app(lichess)
