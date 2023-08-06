# Libraries
import requests  # To get data from website

try:
    url = requests.get("https://yobit.net/api/3/ticker/btc_usd")  # url to the website the data will be gained from
    response = url.json()  # formating data into json
    price = response["btc_usd"]["sell"]  # sorting data by info about btc in currency usd
    print(f"Current BTC price is {price}$")
except requests.exceptions.ConnectionError:  # if there's no connection
    print("No connection to network!")

