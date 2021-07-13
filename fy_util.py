from fyers_api import fyersModel
import pickle
import pandas as pd
from fy_gen_token import fyers_auth_main

with open('fyers_token.pickle', 'rb') as f:
    token = pickle.load(f)

is_async = False
fyers = fyersModel.FyersModel(is_async)


def get_positions(fyers_token):
    holdings = fyers.holdings(token=fyers_token)
    funds = fyers.funds(token=fyers_token)
    i = 0
    j = 0
    unrealized_profit = 0
    realized_profit = 0
    open_positions = []
    open_positions_qty = []

    try:
        if holdings['data']['holdings']:
            print("Holdings: ", holdings)
        else:
            print("There are currently no holdings.\n")
        positions = fyers.positions(token=fyers_token)
        # print(positions)

        if positions['data']['netPositions']:
            while i < len(positions['data']['netPositions']):
                unrealized_profit = unrealized_profit + positions['data']['netPositions'][i]['unrealized_profit']
                realized_profit = realized_profit + positions['data']['netPositions'][i]['realized_profit']
                open_positions.append(positions['data']['netPositions'][i]['id'])
                open_positions_qty.append(positions['data']['netPositions'][i]['qty'])
                i += 1
            open_positions_dict = {open_positions[i]: open_positions_qty[i] for i in range(len(open_positions))}
            print("Unrealized Profit: ", unrealized_profit)
            print("Realized Profit: ", realized_profit)
            print("Open Positions:")
            for j in open_positions_dict:
                print(f"{j} with quantity of {open_positions_dict[j]}")

        else:
            print("There are no open positions")

    except IndexError:
        print("Data has been refreshed. Plz try again tomorow.")
    except TypeError:
        print("Data Unavailable. Generate the token and try again")

    print("Available Amount: ", funds['data']['fund_limit'][0]['equityAmount'])


def alerts(profile_usr):
    try:
        if profile_usr['data']['result']['password_expiry_days'] < 6:
            print(f"***** {profile_usr['data']['result']['password_expiry_days']} days to go for password expiry *****")
            print("Change your password now.")
    except TypeError:
        print("Data Unavailable. Generate the token and try again")


profile = fyers.get_profile(token=token)



