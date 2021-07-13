from fyers_api import accessToken
from selenium import webdriver
from decouple import config
import time
import re
import pickle
import sys

app_id = None
app_secret = None


USER = config('USER')
PASSWORD = config('PASSWORD')
PANCHECK = config('PANCHECK')
PANCARD = config('PANCARD')
# DOB = config('DOB')


def get_app_id_secret():
    """
    This function reads the application id and secret key from file

    :return: None
    """
    global app_id, app_secret
    file = open('auth.txt', 'r')
    app_id = file.readline().split(':')[1].strip()
    app_secret = file.readline().split(':')[1].strip()


def extract_token(full_url):
    """
    This function retrieves the access token generated from the link after authentication is completed with Fyers

    :param full_url: URL generated containing access token after Fyers authentication is complete
    :return: None
    """
    access_token = re.search(r'(?<=https://trialapp.in/\?access_token=).*?(?=user_id=DS03505)', full_url).group(0)
    if access_token:
        with open('fyers_token.pickle', 'wb') as f:
            pickle.dump(access_token, f)
    else:
        print("No token generated")


def generate_token_url(appid, secret_id):
    """
    This function is to automate the login process with Fyers  in order to generate the access token for using the app

    :param appid: Application id of app created in Fyers
    :param secret_id: Secret id of app created in Fyers
    :return: URL containing access token
    """
    driver = webdriver.Chrome()
    app_session = accessToken.SessionModel(appid, secret_id)
    response = app_session.auth()
    if response['code'] != 200:
        print('Error!!! Exiting the program')
        sys.exit()
    auth_code = response['data']['authorization_code']
    app_session.set_token(auth_code)
    gen_token_url = app_session.generate_token()
    driver.get(gen_token_url)

    user_name = driver.find_element_by_id('fyers_id')
    password = driver.find_element_by_id('password')
    pan_card = driver.find_element_by_id('pancard')
    submit_btn = driver.find_element_by_id('btn_id')

    user_name.send_keys(USER)
    password.send_keys(PASSWORD)
    pan_card.send_keys(PANCARD)
    submit_btn.click()
    time.sleep(5)

    url_with_token = driver.current_url
    driver.quit()

    return url_with_token


def fyers_auth_main():
    try:
        get_app_id_secret()
        fyers_url = generate_token_url(app_id, app_secret)
        extract_token(fyers_url)
    except AttributeError:
        print("Your password may have expired or needs to be updated. Plz change the password from Fyers Portal. "
              "This could be a temporary issue as well. Plz try after sometime")




