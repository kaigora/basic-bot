from websockets import Data
import yfinance as yf
import pandas_ta as ta
import json
import os
#from analytics.MarketAnalyst import MarketAnalyst
from utils.data.DataFetcher import DataFetcher
from analytics.MarketAnalyst import MarketAnalyst

CONFIG_FILE_TECH = 'config_technology.json'

data_loader = DataFetcher(config_file=CONFIG_FILE_TECH)
data_loader.fetch_data()