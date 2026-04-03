from datetime import datetime, timedelta
from massive import RESTClient
import finnhub, textwrap, os, json
import pandas as pd
from google import genai
from dotenv import load_dotenv
import requests





# finnhub_client = finnhub.Client(api_key="d6hh259r01qr5k4bu700d6hh259r01qr5k4bu70g")
# client = RESTClient("2aIARFFPjUg07BiZdvLFD6tuC3HRxPgd")
# three_months_ago = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
# today = datetime.now().strftime('%Y-%m-%d')
# past_days = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')


# CISD XNYS

'''
1. To be used for fetching news related to user portfolio

related_companies = client.get_related_companies(
	"AAPL"
	)

'''



# tickers = []
# for t in client.list_tickers(
# 	market="stocks",
#     exchange="XTSE",
# 	active="true",
# 	order="asc",
# 	limit="100",
# 	sort="ticker",
# 	):
#     tickers.append(t)

# print(len(tickers))

# for i, ticker in enumerate(tickers):
#     print(f"{i}: {ticker.ticker}")
#     if i >= 10:
#         break

# poly_news = []
# for n in client.list_ticker_news(
#     #ticker="VOO",
# 	order="asc",
# 	limit="10",
# 	sort="published_utc",
#     published_utc_gte=past_days
# 	):
#     poly_news.append(n)



# poly_publishers = set()
# for n in poly_news:
#     poly_publishers.add(n.publisher.name)

# print(f'number of polygon news: {len(poly_news)}')
# print(f'number of polygon source: {len(poly_publishers)}')
# print('Polygon Sources:')
# for p in poly_publishers:
#     print(p)

# print('='*20)

# finnhub_news = finnhub_client.general_news('general', min_id=0)
# finnhub_publishers = set()
# for n in finnhub_news:
#     finnhub_publishers.add(n['source'])

# print(f'number of finnhub news: {len(finnhub_news)}')
# print(f'number of finnhub source: {len(finnhub_publishers)}')
# print('Finnhub Sources:')
# for p in finnhub_publishers:
#     print(p)

# for index, item in enumerate(news):
#     # verify this is an agg
#     if isinstance(item, TickerNews):
#         print("{:<25}{:<15}{:<15}".format(item.published_utc, item.title, item.publisherName))

#         if index == 20:
#             break

# prompt = textwrap.dedent(f"""
#     SYSTEM:
#     You are a disciplined Swing Trading AI Agent.
    
#     RULES:
#     1. Technicals dictate the TREND.
#     2. Fundamentals dictate the CATALYST.
    
#     =========================================
#     TARGET ASSET: {ticker}
#     CURRENT PRICE: ${current_price:.2f}
#     =========================================
#     """)



# technicals = {
#     "Close Price": [
#         259.88,
#         260.83,
#         260.81,
#         255.76,
#         250.12
#     ],
#     "VWMA_20": [
#         265.26223885467033,
#         264.64196520492203,
#         264.1766533052802,
#         263.10917033766304,
#         262.66507446720914
#     ],
#     "VWMA_50": [
#         263.331265332804,
#         263.2213393321715,
#         263.10411555107765,
#         262.87637811688415,
#         262.59071919142565
#     ],
#     "BBANDS_upper_20_2": [
#         277.80045158355875,
#         276.51833894388676,
#         275.24679915066497,
#         273.5498650727617,
#         274.54888709381396
#     ],
#     "BBANDS_lower_20_2": [
#         253.4995484164412,
#         253.40266105611326,
#         253.38720084933504,
#         253.1101349272384,
#         250.9501129061861
#     ]
# }


# df = pd.DataFrame(technicals)
# df_str = df.to_markdown()
# print(df_str)

# load_dotenv()

# client = genai.Client(api_key="AIzaSyAN2dAUHQhmeSS4QuMWXiJCtSJyVAVMiDo")

# response = client.models.generate_content(
#     model="gemini-3-flash-preview",
#     contents="Explain how AI works in a few words",
# )

# print(response.text)





# assets = requests.get(
#     "http://61.169.200.18:61067/api/v1/available-assets",
#     headers={
#       "Authorization": "Bearer ak_0cd21ba2bf7d6bfb25834a27729c2f276989d6952b18f487138b6f48511c666f"
#     }
# )

# print(assets.json()['assets'][0])


# info = requests.get(
#     "http://61.169.200.18:61067/api/v1/my-participant-info",
#     headers={
#       "Authorization": "Bearer ak_0cd21ba2bf7d6bfb25834a27729c2f276989d6952b18f487138b6f48511c666f"
#     }
# )

# print(info.json())


# ptf = requests.get(
#     "http://61.169.200.18:61067/api/v1/my-portfolio",
#     headers={
#       "Authorization": "Bearer ak_0cd21ba2bf7d6bfb25834a27729c2f276989d6952b18f487138b6f48511c666f"
#     }
# )

# print(ptf.json())


# response = requests.post("http://61.169.200.18:61067/api/v1/orders",
#     headers={
#       "Content-Type": "application/json",
#       "Authorization": "Bearer ak_0cd21ba2bf7d6bfb25834a27729c2f276989d6952b18f487138b6f48511c666f"
#     },
#     json={
#         "items": [
#       {
#         "assetCode": "TSLA",
#         "side": "BUY",
#         "orderAmount": 1000,
#         "referencePrice": 247.99
#       }
#     ]

#     }
# )


# print(response.json())

# requests.post("http://61.169.200.18:61067/api/v1/cancel",
#     headers={
#       "Content-Type": "application/json",
#       "Authorization": "Bearer ak_0cd21ba2bf7d6bfb25834a27729c2f276989d6952b18f487138b6f48511c666f"
#     }
# )



FOLDER_PATH = './configs/'
all_stock_configs = os.listdir(FOLDER_PATH)



