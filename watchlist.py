import os, logging

from pathlib import Path
from dotenv import load_dotenv
from utils.utils import add_stocks, new_watchlist, remove_stocks

# --- Configuration & Setup ---
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Path handling
CONFIG_DIR = Path("./config")

# --- Instructions ---
# Modifies the following parameters to suit your needs
# Enter the file name that you want to modify or create, currently only support the following actions once at a time
# i.e. modify only one file at a time
# 1. If you want to create a new file, enter the the file name in FILE_NAME (e.g. "config_mine_1") and you list of stocks in STOCK_LIST ["BHP","RIO","FCX","SCCO","VALE","TECK","NEM","GOLD","AEM","PAAS"]
# 2. If you want to modify a existing file, enter the file name in FILE_NAME and your list of stocks to add/remove in STOCK_TO_ADD/STOCK_TO_REMOVE respectively
# (STOCK_LIST, STOCK_TO_ADD, STOCK_TO_REMOVE share the same format)
# (It's recommended to have at most 10 stocks in one file, for LLM to process infomation more efficiently)
FILE_NAME = "config_mine_1"
SECTOR = "Mining"
STOCK_LIST = ["BHP","RIO","FCX","SCCO","VALE","TECK","NEM","GOLD","AEM","PAAS"]
STOCK_TO_ADD = [] 
STOCK_TO_REMOVE = [] 
ACTION = "CREATE" # This can be "CREATE" or "MODIFY". Create new file or modify (add/remove) existing file



def main():
    if ACTION.upper() not in ["CREATE", "MODIFY"]:
        logger.error(f"ACTION: '{ACTION}' not recognized, choose from 'CREATE' or 'MODIFY'.")
        return

    if not FILE_NAME:
        logger.error(f"Please provide a FILE_NAME to proceed.")
        return
    
    if len(STOCK_LIST) == 0 and len(STOCK_TO_ADD) == 0 and len(STOCK_TO_REMOVE) == 0:
        logger.error("No stock information provided, check instruction and add stock information.")
        return
    
    file_name = f"{FILE_NAME}.json"
    
    if ACTION == "CREATE":
        new_watchlist(file_name, SECTOR, STOCK_LIST)
        logger.info(f"New watchlist {FILE_NAME} has been created with the following stocks: {', '.join(STOCK_LIST)}.")

    elif ACTION == "MODIFY":
        file_name = CONFIG_DIR / f"{FILE_NAME}.json"

        if len(STOCK_TO_ADD) > 0:
            add_stocks(file_name, STOCK_TO_ADD)
            logger.info(f"{', '.join(STOCK_TO_ADD)} has been added to {FILE_NAME}.")

        if len(STOCK_TO_REMOVE) > 0:
            removed = remove_stocks(file_name,STOCK_TO_REMOVE)
            logger.info(f"{', '.join(STOCK_TO_REMOVE)} has been removed from {FILE_NAME}.")

if __name__ == "__main__":
    main()