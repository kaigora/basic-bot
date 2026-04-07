import json
from pathlib import Path
from datetime import datetime

default_ta = {
    "RSI": [
        14
    ],
    "MACD": [
        {
            "fast_period": 12,
            "slow_period": 26,
            "signal_period": 9
        }
    ],
    "STOCH": [
        {
            "k_period": 14,
            "d_period": 3,
            "smooth_k": 3
        }
    ],
    "EMA": [
        20,
        50,
        200
    ],
    "VWAP": [],
    "VWMA": [
        20,
        50,
        200
    ],
    "HMA": [
        20
    ],
    "ADX": [
        14
    ],
    "BBANDS": [
        {
            "period": 20,
            "stddev": 2
        }
    ],
    "ATR": [
        14
    ],
    "CMF": [
        20
    ],
    "OBV": [],
    "ZSCORE": [
        30
    ]
}

def add_stocks(watchlist:str, stocks:list[str], ta:list[dict]=None)->None:
    if ta and len(ta) != 1 and len(ta) != len(stocks):
        raise ValueError(
            f"Input length mismatch: {len(stocks)} != {len(ta)}"
            f"When ta is provided, length must equal to 1 or length of stock list"
        )
    
    try:
        with open(watchlist, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Error: The file '{watchlist}' was not found.")

    today_date = datetime.today().strftime("%Y-%m-%d")

    for i in range(len(stocks)):
        if ta is None:
            t = default_ta
        elif len(ta) == 1:
            t = ta
        else:
            t = ta[i]

        data["stocks"][stocks[i]] = {
            "new": True,
            "watching_since": today_date,
            "fetch_news": False,
            "fetch_earnings": False,
            "fetch_headlines": False,
            "technical_indicators":t
        }
    
    with open(watchlist, 'w') as outfile:
        json.dump(data, outfile, indent=4)

        

def update_ta():
    pass



def update_status():
    pass



def remove_stocks(watchlist:str, stocks:list[str])->list[str]:
    try:
        with open(watchlist, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Error: The file '{watchlist}' was not found.")

    removed=[]

    if data['stocks']: print("OK")

    for s in stocks:
        if s not in data['stocks']:
            print(f"{s} does not exist in '{watchlist}'")
        else:
            data['stocks'].pop(s)
            removed.append(s)

    with open(watchlist, 'w') as outfile:
        json.dump(data, outfile, indent=4)
    
    return removed



def new_watchlist(file_name:str, sector:str, stocks:list[str], ta:list[dict]=None)->None:
    if ta and len(ta) != 1 and len(ta) != len(stocks):
        raise ValueError(
            f"Input length mismatch: {len(stocks)} != {len(ta)}"
            f"When ta is provided, length must equal to 1 or length of stock list"
        )
    
    if Path(f'./configs/{file_name}').exists():
        raise ValueError(
            f"The file name '{file_name}' is already used"
        )
    
    today_date = datetime.today().strftime("%Y-%m-%d")

    watchlist = {
        "last_updated": today_date,
        "sector": sector,
        "stocks":{}
    }

    for i in range(len(stocks)):
        if ta is None:
            t = default_ta
        elif len(ta) == 1:
            t = ta
        else:
            t = ta[i]

        watchlist["stocks"][stocks[i]] = {
            "new": True,
            "watching_since": today_date,
            "fetch_news": False,
            "fetch_earnings": False,
            "fetch_headlines": False,
            "technical_indicators":t
        }
    
    file_name = f'./configs/{file_name}'

    with open(file_name, 'w') as outfile:
        json.dump(watchlist, outfile, indent=4)

    

def get_watchlist():
    pass



def get_all_stocks():
    pass