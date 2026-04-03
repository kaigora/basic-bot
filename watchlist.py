from utils.utils import add_stocks, new_watchlist, remove_stocks

CONFIG_FILE_TECH_1 = './configs/config_technology_1.json'
CONFIG_FILE_BANK_1 = './configs/config_bank_1.json'




# new_watchlist('config_bank_1.json', 'Bank', ['JPM', 'RY', 'BAC', 'TD', 'BMO', 'WFC', 'BNS', 'ING', 'C', 'MS'])

add_stocks(CONFIG_FILE_TECH_1, ['RIVN'])
removed = remove_stocks(CONFIG_FILE_TECH_1,['RIVN'])
print(removed)