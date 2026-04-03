import os, json, textwrap
import pandas as pd
import numpy as np
import pandas_ta as ta
from dotenv import load_dotenv
from datetime import datetime, timedelta

class MarketAnalyst:
    def __init__(self, config_file:str = None):
        load_dotenv()
        self.config_file = config_file
        self.config_data = None
        self.local_db_path = os.getenv('LOCAL_DB_PATH')
        self.data = {}
        self.load_config()
        
    
    def load_config(self) -> None:
        try:
            with open(self.config_file, 'r') as file:
                self.config_data = json.load(file)
        except FileNotFoundError:
            print(f"Error: The file '{self.config_file}' was not found.")
        except json.JSONDecodeError:
            print(f"Error: Failed to decode JSON from the file. Check if the JSON is valid using a [JSON validator](https://jsonformatter.curiousconcept.com).")



    def load_analysis(self)->None:
        pass



    def load_data(self) -> None:
        tickers = self.config_data["stocks"].keys()
        for ticker in tickers:
            self.data[ticker] = pd.read_csv(f'{self.local_db_path}{ticker}.csv', index_col='timestamp')



    def get_data_from_csv(self, ticker:str) -> pd.DataFrame:
        try:
            df = pd.read_csv(f'{self.local_db_path}{ticker}.csv', index_col='timestamp')
            return df
        except FileNotFoundError:
            print(f"Error: The file for ticker '{ticker}' was not found in the local database.")
            return pd.DataFrame()  # Return an empty DataFrame if the file is not found
        except Exception as e:
            print(f"An error occurred while loading data for ticker '{ticker}': {e}")
            return pd.DataFrame()  # Return an empty DataFrame in case of any other exceptions



    def calculate_technicals_custom(self, bull_bear:bool = False, indicator:dict = {"SMA": [20, 50], "RSI": 14}) -> dict:
        pass



    def ta_engine(self, ticker:str, ta_dict:dict, lookback_period:int = 5) -> dict:
        stock_data = self.get_data_from_csv(ticker)
        ta_results = {}
        ta_results['timestamp'] = stock_data.index[-lookback_period:].to_list()
        ta_results['Close Price'] = stock_data['close'][-lookback_period:].to_list()
        ta_results['Volume'] = stock_data['volume'][-lookback_period:].round().astype(int).to_list()
        for indicator, params_list in ta_dict.items():
            if indicator == "RSI":
                for p in params_list:
                    ta_results[f"RSI_{p}"] = ta.rsi(stock_data['close'], length=p)[-lookback_period:].to_list()
            elif indicator == "MACD":
                for p in params_list:
                    macd = ta.macd(stock_data['close'], fast=p["fast_period"], slow=p["slow_period"], signal=p["signal_period"])
                    ta_results[f"MACD_{p['fast_period']}_{p['slow_period']}_{p['signal_period']}"] = macd[f'MACD_{p["fast_period"]}_{p["slow_period"]}_{p["signal_period"]}'][-lookback_period:].to_list()
                    ta_results[f"MACD_signal_{p['fast_period']}_{p['slow_period']}_{p['signal_period']}"] = macd[f'MACDs_{p["fast_period"]}_{p["slow_period"]}_{p["signal_period"]}'][-lookback_period:].to_list()
            elif indicator == "STOCH":
                for p in params_list:
                    stoch = ta.stoch(stock_data['high'], stock_data['low'], stock_data['close'], k=p["k_period"], d=p["d_period"], smooth_k=p["smooth_k"])
                    ta_results[f"STOCH_k_{p['k_period']}_{p['d_period']}_{p['smooth_k']}"] = stoch[f'STOCHk_{p["k_period"]}_{p["d_period"]}_{p["smooth_k"]}'][-lookback_period:].to_list()
                    ta_results[f"STOCH_d_{p['k_period']}_{p['d_period']}_{p['smooth_k']}"] = stoch[f'STOCHd_{p["k_period"]}_{p["d_period"]}_{p["smooth_k"]}'][-lookback_period:].to_list()
            elif indicator == "EMA":
                for p in params_list:
                    ta_results[f"EMA_{p}"] = ta.ema(stock_data['close'], length=p)[-lookback_period:].to_list()
            elif indicator == "VWAP":
                ta_results["VWAP"] = stock_data["vwap"][-lookback_period:].to_list()
            elif indicator == "VWMA":
                for p in params_list:
                    ta_results[f"VWMA_{p}"] = ta.vwma(stock_data['close'], stock_data['volume'], length=p)[-lookback_period:].to_list()
            elif indicator == "HMA":
                for p in params_list:
                    ta_results[f"HMA_{p}"] = ta.hma(stock_data['close'], length=p)[-lookback_period:].to_list()
            elif indicator == "ADX":
                for p in params_list:
                    adx = ta.adx(stock_data['high'], stock_data['low'], stock_data['close'], length=p)
                    ta_results[f"ADX_{p}"] = adx[f'ADX_{p}'][-lookback_period:].to_list()
                    ta_results[f"ADXR_{p}_2"] = adx[f"ADXR_{p}_2"][-lookback_period:].to_list()
                    ta_results[f"DMP_{p}"] = adx[f"DMP_{p}"][-lookback_period:].to_list()
                    ta_results[f"DMN_{p}"] = adx[f"DMN_{p}"][-lookback_period:].to_list()
            elif indicator == "BBANDS":
                for p in params_list:
                    bbands = ta.bbands(stock_data['close'], length=p["period"], lower_std=p["stddev"], upper_std=p["stddev"])
                    ta_results[f"BBANDS_upper_{p['period']}_{p['stddev']}"] = bbands[f'BBU_{p["period"]}_{p["stddev"]}_{p["stddev"]}'][-lookback_period:].to_list()
                    ta_results[f"BBANDS_middle_{p['period']}_{p['stddev']}"] = bbands[f'BBM_{p["period"]}_{p["stddev"]}_{p["stddev"]}'][-lookback_period:].to_list()
                    ta_results[f"BBANDS_lower_{p['period']}_{p['stddev']}"] = bbands[f'BBL_{p["period"]}_{p["stddev"]}_{p["stddev"]}'][-lookback_period:].to_list()
            elif indicator == "ATR":
                # Check if ATR with mamode = EMA is the same as EMA results, if so we can set the mamode to rolling.
                for p in params_list:
                    ta_results[f"ATR_{p}"] = ta.atr(stock_data['high'], stock_data['low'], stock_data['close'], length=p)[-lookback_period:].to_list()
            elif indicator == "CMF":
                for p in params_list:
                    ta_results[f"CMF_{p}"] = ta.cmf(stock_data['high'], stock_data['low'], stock_data['close'], stock_data['volume'], length=p)[-lookback_period:].to_list()
            elif indicator == "OBV":
                ta_results[f"OBV"] = ta.obv(stock_data['close'], stock_data['volume'])[-lookback_period:].to_list()
            elif indicator == "ZSCORE":
                for p in params_list:
                    ta_results[f"ZScore_{p}"] = ta.zscore(stock_data['close'], length=p)[-lookback_period:].to_list()

        return ta_results



    def calculate_technicals(self, anchor_date:str = None) -> dict:
        anchor_date = datetime.today() if anchor_date is None else datetime.strptime(anchor_date, '%Y-%m-%d')
        results = {}
        for ticker, stock_dict in self.config_data["stocks"].items():
            results[ticker] = self.ta_engine(ticker, stock_dict['technical_indicators'])

        # For checking ta analysis output
        with open("ta_data.json", "w") as file:
            json.dump(results, file, indent=4)

        return results



    def analyse_technical(self, price, technicals):
        results = {
            "momentum": -1, # -1: Bearish; 1: Bullish
            "volatility": -1, # -1: Not Volatile; 1: Volatile
            "trajectory_5d": 0.00 # in %, e.g. 1.2 means 1.2% increase in stock price over past 5 days
            }

        if technicals["VWMA_20"][-1] >= technicals["VWMA_50"][-1]:
            results["momentum"] = 1

        if price >= technicals["BBANDS_upper_20_2"][-1] or price <= technicals["BBANDS_lower_20_2"][-1]:
            results["volatility"] = 1

        results["trajectory_5d"] = (technicals['Close Price'][-1] / technicals['Close Price'][0] - 1) * 100.00
        
        return results



    def generate_llm_prompt(self, techinicals:dict, headlines:list[str] = None, news:list[str] = None) -> str:
        prompt = textwrap.dedent(f"""
        SYSTEM:
        You are a disciplined, risk-averse Swing Trading AI Agent. 
        Your objective is to scan a watchlist of assets using strictly technical data to identify high-probability swing trading setups.
        
        RULES:
        1. Base your decisions purely on the provided technical trajectories, volume, and volatility (Bollinger Bands).
        2. Never suggest a "BUY" if the price is in the OVERBOUGHT Bollinger Band zone.
        3. A "BUY" signal requires bullish momentum (e.g., 20 VWMA > 50 VWMA) and volume confirmation.
        4. You must output your decision strictly as a JSON array containing one evaluation object per asset.

        =========================================
        MARKET DATA TO ANALYSE:
        =========================================
        """)

        for stock, ta in techinicals.items():
            price = ta["Close Price"][-1]

            prompt += f"\nTARGET ASSET: {stock}\n"
            prompt += f"\nLATEST CLOSE PRICE: {price}\n"

            
            prompt += "\n1. TECHNICAL CONTEXT (Pre-Calculated):\n"
            analysis = self.analyse_technical(price, ta)
            if analysis["momentum"] == 1:
                prompt += f"\n- Momentum: BULLISH (The 20-period VWMA has crossed ABOVE the 50-period VWMA).\n"
            elif analysis["momentum"] == -1:
                prompt += f"\n- Momentum: BEARISH (The 20-period VWMA has not crossed ABOVE the 50-period VWMA).\n"
            if analysis["volatility"] == 1:
                prompt += "\n- Volatility: VOLATILE (Current price is outside of the Upper and Lower Bollinger Bands).\n"
            elif analysis["volatility"] == -1:
                prompt += "\n- Volatility: NEUTRAL (Current price is sitting comfortably between the Upper and Lower Bollinger Bands).\n"
            prompt += f"\n- 5-Day Trajectory: Price has {"increaed" if analysis["trajectory_5d"] >= 0 else "decreased"} by {np.abs(analysis["trajectory_5d"])}% on slightly decreasing volume.\n"
            
            prompt += "\n2. RECENT PRICE ACTION (Last 5 Periods):\n"

            ta_df = pd.DataFrame(ta)
            ta_str = ta_df.to_markdown()
            prompt += f"\n{ta_str}\n"

            prompt += "\n-----------------------------------------\n"
            

        task_str = "technical data"

        if headlines:
            task_str += ", headlines"
            prompt += "\nRecent Headlines:\n"
            for i, headline in enumerate(headlines, 1):
                prompt += f"{i}. {headline}\n"

        if news:
            task_str += ", news"
            prompt += "\nRecent News:\n"
            for i, item in enumerate(news, 1):
                prompt += f"{i}. {item}\n"

        

        prompt += textwrap.dedent(f"""
                                 
        =========================================
        TASK:
        Analyze the {task_str} for all provided assets. Output your final decisions in the following JSON array schema exactly. Do not include any markdown formatting or text outside of the JSON array.
        """)
        return prompt