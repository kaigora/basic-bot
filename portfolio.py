import os, logging, requests, yaml

import pandas as pd

from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

# --- Configuration & Setup ---
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Path handling
OUTPUT_DIR = Path('./portfolio/')

# --- Instructions ---
SAVE_TO_FILE = True



def get_portfolio(save_to_file:bool) -> dict:
    logger.info("Loading portfolio info from Kaigora...")

    try:
        kaigora_response = requests.get(
            "https://kaigora.com/api/v1/my-portfolio",
            headers={
              "Authorization": f"Bearer {os.getenv('KAIGORA_API_KEY')}"
            }
        )

        kaigora_response.raise_for_status()
        logger.info(f"Successfully loaded portfolio info. API Response: {kaigora_response.status_code}")

    except Exception as e:
        logger.error(f"Fail to load portfolio data due to: {e}")
        return {}

    portfolio = kaigora_response.json()

    if save_to_file:
        logger.info("Saving portfolio info to file...")
        today = datetime.now().strftime('%Y-%m-%d')
        file_name = OUTPUT_DIR / f"{today}.yaml"
        try:
           with open(file_name,'w') as file:
               yaml.dump(portfolio, file, default_flow_style=False, sort_keys=False)

        except Exception as e:
            logger.error("Fail to save portfolio info to file due to: {e}")

    return portfolio



def print_json_recursion(data:dict, indent:int=4, initial_indent:int=0)->None:
    spaces = " " * initial_indent

    if isinstance(data, dict):
        for k,v in data.items():
            if isinstance(v,(dict,list)):
                print(f"{spaces}{k}:")
                print_json_recursion(v, indent, initial_indent+indent)
            else:
                print(f"{spaces}{k}:{v}")

    elif isinstance(data, list):
        for idx, itm in enumerate(data):
            if isinstance(itm,(list,dict)):
                print(f"{spaces}[Item {idx}]")
                print_json_recursion(itm, indent, initial_indent+indent)

            else:
                print(f"{spaces}{itm}")

    else:
        print(f"{spaces}{data}")



def main():
    portfolio = get_portfolio(SAVE_TO_FILE)
    print_json_recursion(portfolio)



if __name__ == "__main__":
    main()
