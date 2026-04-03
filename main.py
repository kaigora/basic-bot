import json, os, time
from websockets import Data
from dotenv import load_dotenv
from google import genai
import yfinance as yf
import pandas_ta as ta
from utils.data.DataFetcher import DataFetcher
from analytics.MarketAnalyst import MarketAnalyst

load_dotenv()
FOLDER_PATH = './configs/'
all_stock_configs = os.listdir(FOLDER_PATH)
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')


generate_prompt_files = True # True: if you want to inspect the prompt, this will generate a .txt file for each prompt; False: if you don't want to generate the .txt file


if __name__ == "__main__":

    technical_list = {}
    prompts = {}

    for c in all_stock_configs:
        data_loader = DataFetcher(config_file=f"{FOLDER_PATH}{c}")
        data_loader.fetch_data()
        if c != all_stock_configs[-1]:
            time.sleep(60) # To make sure API call stays in the limit of 5 times per min, remove if you have paid version
        
        market_analyst = MarketAnalyst(config_file=f"{FOLDER_PATH}{c}")
        market_analyst.load_data()
        technical = market_analyst.calculate_technicals()
        technical_list[c] = technical
        prompts[c] = market_analyst.generate_llm_prompt(technical)
    
    client = genai.Client(api_key=GEMINI_API_KEY)
    responses = {}

    for k in prompts:
        resp = client.models.generate_content(
            model="gemini-3.1-pro-preview",
            contents=p
        )
        responses[k] = resp.text

        if generate_prompt_files:
            with open(f"{k}.txt", "w") as file:
                file.write(resp.text)


