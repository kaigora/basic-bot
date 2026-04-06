import os, json, time
import pandas as pd
from polygon import RESTClient  
from dotenv import load_dotenv
from datetime import datetime, timedelta

# datafetcher should run daily to fetch past date's data for existing tickers in the config file and save in database
# For new tikcers, it should fetch 1 year of daily historical data and save in database, then set the config file to indicate that the ticker is existing

class DataFetcher:
    def __init__(self, config_file=None):
        self.config_file = config_file
        self.config_data = None
        load_dotenv()
        self.client = RESTClient(os.getenv('POLYGON_API_KEY'))
        self.local_db_path = os.getenv('LOCAL_DB_PATH')
        self.load_config()


    
    def dynamic_indicator_adjustor(self) -> None:
        # TODO: To make the technical indicators more dynamic, we can adjust the parameters based on the stock's volatility, trading volume, or other relevant factors. For example, we can use a shorter period for SMA during high volatility and a longer period during low volatility. This can help to capture the trends more accurately and provide better insights for analysis.
        pass
    


    def load_config(self) -> None:
        try:
            with open(self.config_file, 'r') as file:
                self.config_data = json.load(file)
        except FileNotFoundError:
            print(f"Error: The file '{self.config_file}' was not found.")
        except json.JSONDecodeError:
            print(f"Error: Failed to decode JSON from the file. Check if the JSON is valid using a [JSON validator](https://jsonformatter.curiousconcept.com).")

    

    def fetch_data_custom(self, tickers:list[str], start_date:list[str]=None, end_date:list[str]=None, to_existing:list[bool]=[True], temp_data:bool=True) -> None:
        '''
        A custom data fetching function, can be used to updated data for specific tickers and specific date range,
        can be used to fix data issues or to run tests
        '''
        aggs = []
        for i, ticker in enumerate(tickers,1):
            for a in self.client.list_aggs(
                ticker=ticker,
                multiplier=1,
                timespan="day",
                from_=start_date[i],
                to=end_date[i],
                limit=50000
            ):
                aggs.append(a)

            df = pd.DataFrame(aggs)
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            if temp_data:
                df.to_csv(f'{self.local_db_path}{ticker}_temp.csv', index=False, mode='a')
            else:
                df.to_csv(f'{self.local_db_path}{ticker}.csv', index=False, header=False, mode='a')



    def fetch_data_bulk(self, date:str = None, distribute:bool=False) -> None:
        if date is None:
            date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        grouped_data = self.client.get_grouped_daily_aggs(date=date)
        df_market = pd.DataFrame(grouped_data)

        '''
        TODO:
            We can download the data for all tickers in the config file and append the new data to the existing files, 
            then update the config file to indicate that the data has been updated for the date. 
            This can help to reduce the number of API calls and make the data fetching process more efficient, 
            when the number of tickers is large and the data is updated daily. 
            We can also implement a check to avoid fetching data for tickers that have already been updated for the date, 
            which can further optimize the process and save time and resources.
        '''
        
        if distribute:
            pass
        else:
            pass
        
        df_market.to_csv(f'{self.local_db_path}market_{date}.csv', index=False, mode='a', header=True)


    def fetch_data(self, start_date:str=None, end_date:str=None, years:int=2, no_skip:bool=False, sleep_time:int=60) -> None:
        # need consistent timestamp for new ticker and exsiting ticker when fetching data.
        today = datetime.now().strftime('%Y-%m-%d')
        start_date = datetime.strptime(start_date, '%Y-%m-%d') if start_date else None
        end_date = datetime.strptime(end_date, '%Y-%m-%d') if end_date else None
        if start_date is None and end_date is None:
            start_date = (datetime.now() - timedelta(days=365*years)).strftime('%Y-%m-%d')
            end_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        if end_date is not None and start_date is None:
            start_date = (end_date - timedelta(days=365*years)).strftime('%Y-%m-%d')
            end_date = end_date.strftime('%Y-%m-%d')

        tickers = list(self.config_data['stocks'].keys())
        
        for i, ticker in enumerate(tickers,1):
            print(f'Fetching data for {ticker} ({i}/{len(tickers)})...')
            aggs = []
            if self.config_data['stocks'][ticker]['new']:
                for a in self.client.list_aggs(
                    ticker=ticker,
                    multiplier=1,
                    timespan="day",
                    from_=start_date,
                    to=end_date,
                    limit=50000
                ):
                    aggs.append(a)

                df = pd.DataFrame(aggs)
                df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
                df.to_csv(f'{self.local_db_path}{ticker}.csv', index=False, header=True)
                self.config_data['stocks'][ticker]['new'] = False
                self.config_data['stocks'][ticker]['watching_since'] = today

            else:
                if self.config_data['last_updated'] == today and not no_skip:
                    print(f"Data for {ticker} has already been fetched for today. Skipping...")
                    continue
                for a in self.client.list_aggs(
                    ticker=ticker,
                    multiplier=1,
                    timespan="day",
                    from_=end_date,
                    to=end_date,
                    limit=50000
                ):
                    aggs.append(a)

                df = pd.DataFrame(aggs)
                df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
                df.to_csv(f'{self.local_db_path}{ticker}.csv', index=False, mode='a', header=False)

            if i % 5 == 0:
                time.sleep(sleep_time)  # Sleep for 1 munites after every 5 tickers to avoid hitting API rate limits

        self.config_data['last_updated'] = today
        with open(self.config_file, 'w') as file:
            json.dump(self.config_data, file, indent=4)

        print(f"Data fetching completed and updated config file: {self.config_file}.")
        

        
        
        