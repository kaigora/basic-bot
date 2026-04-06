import json, os, time, logging, requests

from typing import Dict

from pathlib import Path
from dotenv import load_dotenv
from google import genai

from utils.data.DataFetcher import DataFetcher
from analytics.MarketAnalyst import MarketAnalyst

# --- Configuration & Setup ---
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Path handling
CONFIG_DIR = Path('./configs/')
OUTPUT_DIR = Path('./outputs/')

# --- Instructions ---
# Modifies the following parameters to suit your needs
SAVE_OUTPUTS = True # True: saves both prompt and the LLM response to file
AUTO_TRADE = False # True: the bot will make final decision and trade based on LLM response. False: user should examines the outputs and use the trade.py to place order.
RATE_LIMIT_DELAY = 60 # Seconds to sleep to respect API limits. Remove/update if you have paied tier or using a different API for data.
LLM_MODEL_NAME = "gemini-3.1-pro-preview" # The specific AI model name you want to use. 
WHICH_API_KEY = "GEMINI_API_KEY" # Which API key in .env is used for LLM response, need to match the variable name of your choice of API Key in .env



def process_stock_data(config_file: Path) -> str:
    """Fetches data and generates an LLM prompt for a stocks config."""

    logger.info(f"Processing data for {config_file.name}...")

    try:
        data_loader = DataFetcher(config_file=str(config_file))
        data_loader.fetch_data(sleep_time=RATE_LIMIT_DELAY)

        market_analyst = MarketAnalyst(config_file=str(config_file))
        market_analyst.load_data()

        technical = market_analyst.calculate_technicals()
        prompt = market_analyst.generate_llm_prompt(technical)

        return prompt
    
    except Exception as e:
        logger.error(f"Fail to process {config_file.name}: {e}")
        return ""



def get_llm_analysis(client: genai.Client, prompt: str, config_file: str) -> str:
    """Queries the LLM API with the generated prompt."""

    logger.info(f"Queries LLM for {config_file}...")

    try:
        response = client.models.generate_content(
            model=LLM_MODEL_NAME,
            contents=prompt
        )

        return response.text
    
    except Exception as e:
        logger.error(f"LLM API call failed for {config_file}: {e}")
        return ""




def generate_order(response: str) -> str:
    pass


def main():

    # 1. Validate API Key
    llm_api_key = os.getenv(WHICH_API_KEY)
    if not llm_api_key:
        raise ValueError(f"{WHICH_API_KEY} environment variable is missing. Check your .env file.")
    
    client = genai.Client(api_key=llm_api_key)

    # 2. Prepare Directories
    if SAVE_OUTPUTS:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    valid_configs = [f for f in CONFIG_DIR.iterdir() if f.is_file and not f.name.startswith('.')]

    if not valid_configs:
        logger.warning(f"No valid configuration files found in {CONFIG_DIR}")
        return
    
    # {config_file.name: prompt}
    prompts: Dict[str, str] = {}
    # {config_file.name: response}
    responses: Dict[str, str] = {}

    # 3. Phase One: Data Processing
    logger.info("----- Starting Data Processing Phase -----")
    for idx, config_path in enumerate(valid_configs):
        prompt = process_stock_data(config_path)

        if prompt:
            prompts[config_path.stem] = prompt
        
        if idx < len(valid_configs) - 1 and RATE_LIMIT_DELAY > 0:
            logger.info(f"Sleeping for {RATE_LIMIT_DELAY} seconds for rate limits...")
            time.sleep(RATE_LIMIT_DELAY)

    # 4. Phase Two: LLM Inference
    logger.info("----- Starting LLM Inference Phase -----")
    for config_file_name, prompt in prompts.items():
        response_text = get_llm_analysis(client, prompt, config_file_name)

        if response_text:
            responses[config_file_name] = response_text

            if SAVE_OUTPUTS:
                prompt_file = OUTPUT_DIR / f"{config_file_name}_prompt.txt"
                prompt_file.write_text(prompt, encoding="utf-8")

                response_file = OUTPUT_DIR / f"{config_file_name}_response.txt"
                response_file.write_text(response_text, encoding="utf-8")

                logger.info(f"Saved outputs for {config_file_name} in {OUTPUT_DIR}")

    if AUTO_TRADE:
        # 5. Phase Three: Generate and Place Order in Kaigora
        # (Only triggered when AUTO_TRADE is True)
        logger.info("----- Starting Auto Trade Phase -----")        
        orders = []
        for config_file_name, response in responses.items():
            orders.append(generate_order())

        try:
            kaigora_response = requests.post("http://61.169.200.18:61067/api/v1/orders",
                headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {os.getenv("KAIGORA_API_KEY")}"
                },
                json={
                    "items": orders
                }
            )
        
        except Exception as e:
            logger.error(f"Order failed to process due to: {e}")


    logger.info("Pipline excution complete.")


if __name__ == "__main__":
    main()