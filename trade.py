import os, logging, requests

import pandas as pd

from pathlib import Path
from dotenv import load_dotenv


# --- Configuration and Setup ---
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Path handling
DATA_DIR = Path('./data/')
OUTPUT_DIR = Path('./outputs/')

# --- Instructions ---
# Modifies the following parameters to suit your needs
# Enter your order here in the format of "[STOCK SYMBOL], [BUY/SELL], [AMOUNT($)]"
# e.g. If you want to buy $10,000 worth of Apple stock enter "AAPL BUY 10000"
# You can place multipe orders by seperating the orders with comma (,) at the end of each order
ORDERS = [
    "AAPL BUY 10000",
    "AMZN BUY 5000",
    # Add to or remove from here based on your examination of the LLM genertaed responses.
]



def get_ref_price(stock:str)->float:
    try:
        file_path = DATA_DIR / f"{stock}.csv"
        df = pd.read_csv(file_path, index_col='timestamp')
        return df['close'].iloc[-1]
    except FileNotFoundError:
        logger.error(f"Error: The data file for {stock} was not found in the local database.")
        return -1.0
    except Exception as e:
        logger.error(f"An error occurred while loading data for {stock}: {e}")
        return -1.0



def format_order_for_api(order_list:list)->list[dict]:
    logger.info("Formating your order...")

    formatted_order = []

    for order in order_list:
        logger.info(f"Preparing order: {order}...")
        try:
            parts = order.split()
            symbol = parts[0].upper()
            action = parts[1].upper()
            amount = float(parts[2])
            reference_price = get_ref_price(symbol)

            if reference_price == -1.0:
                logger.warning(f"Skipping {order} due to missing reference price.")
                continue

            if action not in ["BUY", "SELL"]:
                logger.warning(f"Skipping '{order}': Action must be BUY or SELL.")
                continue

            formatted_order.append(
            {
                "assetCode": symbol,
                "side": action,
                "orderAmount": amount,
                "referencePrice": reference_price
            }
            )

        except Exception as e:
            logger.error(f"Order format for {order} failed due to: {e}")

        

    return formatted_order



def main():
    logger.info("----- Starting Manual Excecution Module -----")

    if not ORDERS:
        logger.error("No orders found in ORDERS list. Exiting.")
        return
    
    logger.info(f"Loaded {len(ORDERS)} trades from script.")

    # 1. Process and validate the inputs
    api_payload_items = format_order_for_api(ORDERS)

    if not api_payload_items:
        logger.error("No valid orders could be parsed. Check your syntax. Exiting.")
        return
    
    # 2. Execute the API Call
    logger.info("Dispatching orders to Kaigora API...")
    try:
        kaigora_response = requests.post("http://61.169.200.18:61067/api/v1/orders",
            headers={
              "Content-Type": "application/json",
              "Authorization": f"Bearer {os.getenv('KAIGORA_API_KEY')}"
            },
            json={
                "items": api_payload_items
            }
        )

        kaigora_response.raise_for_status()
        logger.info(f"Successfully placed orders. API Response: {kaigora_response.status_code}")
    
    except Exception as e:
        logger.error(f"Order failed to process due to network/API error: {e}")


if __name__ == "__main__":
    main()