import requests



# response = requests.get(
#     "http://61.169.200.18:61067/api/v1/my-participant-info",
#     headers={
#       "Authorization": "Bearer ak_0cd21ba2bf7d6bfb25834a27729c2f276989d6952b18f487138b6f48511c666f"
#     }
# )

# orders = response.json()['pendingOrders']
# for o in orders:
#     print(f'{o['assetCode']} order ID: {o['orderId']}')


# orderId = 'ageblk75qaqfrqk5dx2lagwx'

# requests.post(
#     f"http://61.169.200.18:61067/api/v1/orders/{orderId}/cancel",
#     headers={
#       "Authorization": "Bearer ak_0cd21ba2bf7d6bfb25834a27729c2f276989d6952b18f487138b6f48511c666f"
#     }
# )


# response = requests.post("http://61.169.200.18:61067/api/v1/orders",
#     headers={
#       "Content-Type": "application/json",
#       "Authorization": "Bearer ak_0cd21ba2bf7d6bfb25834a27729c2f276989d6952b18f487138b6f48511c666f"
#     },
#     json={
#         "items": [
#       {
#         "assetCode": "RIVN",
#         "side": "BUY",
#         "orderAmount": 99900,
#         "referencePrice": 15.62
#       },
#       {
#         "assetCode": "TD",
#         "side": "BUY",
#         "orderAmount": 99900,
#         "referencePrice": 130.32
#       },
#       {
#         "assetCode": "BMO",
#         "side": "BUY",
#         "orderAmount": 99900,
#         "referencePrice": 189.47
#       },
#       {
#         "assetCode": "PLTR",
#         "side": "BUY",
#         "orderAmount": 99900,
#         "referencePrice": 154.96
#       },
#       {
#         "assetCode": "ISRG",
#         "side": "BUY",
#         "orderAmount": 99900,
#         "referencePrice": 916.31
#       },
#       {
#         "assetCode": "NVO",
#         "side": "BUY",
#         "orderAmount": 99900,
#         "referencePrice": 36.33
#       },
#       {
#         "assetCode": "CRSP",
#         "side": "BUY",
#         "orderAmount": 99900,
#         "referencePrice": 47.09
#       },
#       {
#         "assetCode": "VRTX",
#         "side": "BUY",
#         "orderAmount": 99900,
#         "referencePrice": 454.97
#       },
#       {
#         "assetCode": "NVDA",
#         "side": "BUY",
#         "orderAmount": 99900,
#         "referencePrice": 178.68
#       },
#       {
#         "assetCode": "ARM",
#         "side": "BUY",
#         "orderAmount": 99900,
#         "referencePrice": 157.07
#       }
#     ]

#     }
# )

# my_ptf = ['TD','BMO','PLTR','ARM','RIVN',"ISRG",'NVDA','VRTX','CRSP','NVO']


response = requests.get(
    "http://61.169.200.18:61067/api/v1/available-assets",
    headers={
      "Authorization": "Bearer ak_0cd21ba2bf7d6bfb25834a27729c2f276989d6952b18f487138b6f48511c666f"
    }
)

available_assets = response.json()['assets']
print(len(available_assets))
# available_ticker = set()

# for i in available_assets:
#     available_ticker.add(i['assetCode'])

# all_available = True

# for i in my_ptf:
#     if i not in available_ticker:
#         print(f'{i} not available')
#         all_available = False

# if all_available: print("all availabe")