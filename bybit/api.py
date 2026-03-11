import requests

def check_symbol(symbol):

    url = "https://api.bybit.com/v5/market/instruments-info"

    params = {
        "category": "linear",
        "symbol": symbol
    }

    r = requests.get(url, params=params)

    data = r.json()

    if data["retCode"] == 0 and data["result"]["list"]:
        return True

    return False