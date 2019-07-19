from requests_html import HTMLSession
import pprint

def fetchUrl(user_url_input):
    session = HTMLSession()
    r = session.get(user_url_input)
    priceEls = r.html.find(".offer_list .Plugin_Price", first=False)
    prices = []
    for i in range(0, len(priceEls)):
        prices.append(float(priceEls[i].text.replace("'",'')))
    prices.sort()
    return prices[0]
url = input("Provide an URL")
pprint.pprint("Current Lowest ist..." +str(fetchUrl(url)))