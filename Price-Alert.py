from requests_html import HTMLSession
import requests
import simplejson as json
import pprint
from lib import RequestHelper 


# DECLARE VARIABLES
STANDARD_HEADER = [{"Content-Type" : "application/x-www-form-urlencoded"}]
USER_ACTIONS = json.loads('[{"Name": "Setup new Alert", "type": "SETUP_ALERT"},{"Name": "View Alerts", "type": "VIEW_ALERTS"},{"Name": "View Single Alert", "type": "VIEW_SINGLE_ALERT"}]')
USER_AUTHENTICATED = False
USER = { 
    'userId' : None ,
    'idToken' : None,
    }
APPLICATION_RUNNING = True


# FETCH NEW ITEM
def fetchUrl(user_url_input):
    session = HTMLSession()
    r = session.get(user_url_input)
    priceEls = r.html.find(".offer_list .Plugin_Price", first=False)
    prices = []
    for i in range(0, len(priceEls)):
        prices.append(float(priceEls[i].text.replace("'", '')))
    prices.sort()
    return prices[0]


def registerUser(email, password):
    # 1 Request Register
    req = RequestHelper.buildRequest(
        "http://127.0.0.1:5000/login",
        [{"register_email": loginName }, 
        {"register_password": password}],
        STANDARD_HEADER)

    # 1.1 On Error
    if (req is None or req.status_code is not 200):
        print("Error Registering User.. Try again.")
        USER_AUTHENTICATED = False
        
    # 1.2 On Success
    else:
        request_result = req.json()
        USER['userId'] = request_result['userId']
        USER['idToken'] = request_result['idToken']
        USER_AUTHENTICATED = True
        print("Sucessfully registered.")


def authenticateUser():
    # 1 Already an account?
    alreadyAccount = input("Do you already have an Account (y/N)")

    # 2 No Account
    if (not alreadyAccount):
        email = input("Choose an Email")
        password = input("Choose a Password (8 Digits)")
        passwordRepeat = input("Repeat the chosen Password")
        if (password == passwordRepeat):
            registerUser(email, password)
        return
    
    # 3 Has Account
    loginName = input("Username:   ")
    password = input("Password:   ")

    # 4 Request Authentification
    req = RequestHelper.buildRequest(
        "http://127.0.0.1:5000/login",
        [{"login_email": loginName }, 
        {"login_password": password}],
        STANDARD_HEADER)

    # 4.1 On Error
    if (req is None or req.status_code is not 200):
        print("Error Authenticating User.. Try again.")
        USER_AUTHENTICATED = False
        
    # 4.2 On Success
    else:
        request_result = req.json()
        USER['userId'] = request_result['userId']
        USER['idToken'] = request_result['idToken']
        USER_AUTHENTICATED = True
        print("Sucessfully logged in.")


while (APPLICATION_RUNNING):
    if (USER_AUTHENTICATED):
        possibilities = " \n"
        for key in USER_ACTIONS.items():
            print(key)
        user_action = input("What do you want to do: " + possibilities)
    else:
        authenticateUser()


url = input("Provide an URL")
pprint.pprint("Current Lowest ist..." +str(fetchUrl(url)))