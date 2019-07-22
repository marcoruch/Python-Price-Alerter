import sys
from requests_html import HTMLSession
import requests
import simplejson as json
import pprint
import pandas as pd
from lib import RequestHelper 
from lib import ConsoleHelper


# DECLARE VARIABLES
STANDARD_HEADER = [{"Content-Type" : "application/x-www-form-urlencoded"}]
AUTHORIZED_HEADER = None

USER_ACTIONS = [
    {"Name": "Setup new Alert", "Type": "SETUP_ALERT", "Function": "CreateAlert"},
    {"Name": "View Alerts", "Type": "VIEW_ALERTS", "Function": "ViewAlerts"},
    {"Name": "View Single Alert", "Type": "VIEW_SINGLE_ALERT", "Function": "ViewSingleAlert"},
    {"Name": "Exit Application", "Type": "EXIT", "Function": "ExitApplication"}]

USER_ACTIONS_DICTIONARY = json.loads(str(USER_ACTIONS).replace("\'", "\""))
USER = { 
    'userId' : None ,
    'idToken' : None,
    'authenticated' : None,
    }
APPLICATION_RUNNING = True

# REGISTER USER BY EMAIL AND PASSWORD
def registerUser(email, password):
    # 1 Request Register
    req = RequestHelper.buildPostRequest(
        "http://127.0.0.1:5000/register",
        [{"register_email": email }, 
        {"register_password": password}],
        STANDARD_HEADER)

    # 1.1 On Error
    if (req is None or req.status_code is not 200):
        USER['authenticated'] = False
        print("Error Registering User.. Try again.")
        
    # 1.2 On Success
    else:
        request_result = req.json()
        USER['userId'] = request_result['userId']
        USER['idToken'] = request_result['idToken']
        USER['authenticated'] = True
        print("Sucessfully registered.")

# LOGIN USER BY EMAIL AND PASSWORD
def authenticateUser():
    # 1 Already an account?
    alreadyAccount = input("Do you already have an Account (y/N)").lower()

    # 2 No Account
    if ("n" == alreadyAccount or "no" == alreadyAccount):
        email = input("Choose an Email:   ")
        password = input("Choose a Password (8 Digits):   ")
        passwordRepeat = input("Repeat the chosen Password:   ")
        if (password == passwordRepeat):
            registerUser(email, password)
        return
    elif ("y" == alreadyAccount or "yes" == alreadyAccount):
        # 3 Has Account
        loginName = input("Username:   ")
        password = input("Password:   ")

        # 4 Request Authentification
        req = RequestHelper.buildPostRequest(
            "http://127.0.0.1:5000/login",
            [{"login_email": loginName }, 
            {"login_password": password}],
            STANDARD_HEADER)

        # 4.1 On Error
        if (req is None or req.status_code is not 200):
            USER['authenticated'] = False
            print("Error Authenticating User.. Try again.")
            
        # 4.2 On Success
        else:
            request_result = req.json()
            USER['userId'] = request_result['userId']
            USER['idToken'] = request_result['idToken']
            global AUTHORIZED_HEADER
            AUTHORIZED_HEADER = [
                {"Content-Type" : "application/x-www-form-urlencoded"},
                {"User-Token":request_result['idToken']},
                {"User-Id":request_result['userId']}]
            USER['authenticated'] = True
            print("Sucessfully logged in.")

def ExitApplication():
    global APPLICATION_RUNNING
    APPLICATION_RUNNING = False

def ViewAlerts():
    req = RequestHelper.buildGetRequest("http://127.0.0.1:5000/alerts",
        None, AUTHORIZED_HEADER)
    # On Error
    if (req is None or req.status_code is not 200):
            print(req)
    # On Success
    else:
        request_result = req.json()
        alert_collection = ""
        for alert in request_result:
            alert = alert['documentData']
            price = CheckCurrentPrice(alert.get("itemUrl"))
            alert_collection += f'{alert.get("itemName")}: \n   Current Price is: - {price} \n   Alert it set at {alert.get("alertPrice")} \n'
            if (price is not None and price <= float(alert['alertPrice'])):
                alert_collection += "!!!!!ALERT!!!!! \n"
        pprint.pprint(alert_collection)
        input("Press any key to get back to the menu...")

def CheckCurrentPrice(alert_url):
    session = HTMLSession()
    r = session.get(alert_url)
    priceEls = r.html.find(".offer_list .Plugin_Price", first=False)
    prices = []
    for i in range(0, len(priceEls)):
        prices.append(float(priceEls[i].text.replace("'", '')))
    prices.sort()
    if (prices is None or len(prices) <=0):
        return None
    return prices[0]
    


def CreateAlert():
    alert_url = input("Toppreise URL:  ")
    alert_currentPrice = CheckCurrentPrice(alert_url)
    if (alert_currentPrice is None or alert_currentPrice <= 0):
        pprint.pprint("Could not fetch Product URL")
        return
    pprint.pprint("Current Lowest ist..." + str(alert_currentPrice))
    alert_price = input("When should the alert go off? (Format like:105.50)")
    alert_name = input("Produktname:   ")

    req = RequestHelper.buildPostRequest("http://127.0.0.1:5000/alerts",
        [
            {"itemUrl": alert_url }, 
            {"alertPrice": alert_price }, 
            {"itemName": alert_name }, 
            {"itemUrl": alert_url },
            {"currentPrice": alert_currentPrice}
        ],
        AUTHORIZED_HEADER)
    # On Error
    if (req is None or req.status_code is not 200):
            print(req)
            
            a = input()
            print("Error Posting alert... Try again")
    # On Success
    else:
        request_result = req.json()
        print("Created document...: " + request_result['documentId'])

def ViewSingleAlert():
    print("ViewSingleAlert")
    input()
    
while (APPLICATION_RUNNING):
    if (USER['authenticated']):
        possibilities = " \n"
        for action in USER_ACTIONS_DICTIONARY:
            possibilities += f'   - {action.get("Name")}: {action.get("Type")} \n'
        
        try:
            user_action_input = input("What do you want to do: " + possibilities).upper()
            for action in USER_ACTIONS_DICTIONARY:
                if (action.get("Type") == user_action_input):
                    ConsoleHelper.clear()
                    locals()[action.get("Function")]()
            
        except Exception as e: 
            pprint.pprint(e)
    else:
        authenticateUser()