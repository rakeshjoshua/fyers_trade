import fy_util
from fy_gen_token import fyers_auth_main

profile = fy_util.profile
token = fy_util.token

if profile['code'] == 401:
    print("Generating token...")
    fyers_auth_main()
    print("Token generated")
elif profile['code'] == 200:
    fy_util.get_positions(token)
    fy_util.alerts(profile)
elif profile['code'] == 500:
    print("Internet is not available. Plz check your connectivity.")
elif profile['code'] != 200:
    print("Unknown exception occured !!!", profile['code'])
