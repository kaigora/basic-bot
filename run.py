import sys
import logging

# Set up logging for the runner
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("Runner")

# Attempt to import the user's modules
try:
    import watchlist
    import main as analysis_main
    import trade
    import portfolio
except ImportError as e:
    logger.error(f"Failed to import required modules: {e}")
    logger.info("Ensure run.py is in the same directory as main.py, portfolio.py, trade.py, and watchlist.py")
    sys.exit(1)


def print_header(title: str):
    print("\n" + "="*50)
    print(f"{title.center(50)}")
    print("="*50)


def handle_watchlist():
    print_header("Watchlist Manager")
    action = input("Do you want to CREATE a new list or MODIFY an existing one? (CREATE/MODIFY): ").strip().upper()
    
    if action not in ["CREATE", "MODIFY"]:
        print("Invalid action selected. Returning to main menu.")
        return

    file_name = input("Enter the watchlist file name (e.g., 'config_mine_1'): ").strip()
    if not file_name:
        print("File name cannot be empty.")
        return

    # Update watchlist.py global variables
    watchlist.ACTION = action
    watchlist.FILE_NAME = file_name

    if action == "CREATE":
        sector = input("Enter the sector name (e.g., 'Mining'): ").strip()
        stocks = input("Enter stock symbols separated by commas (e.g., AAPL,MSFT,TSLA): ").strip().upper()
        
        watchlist.SECTOR = sector
        watchlist.STOCK_LIST = [s.strip() for s in stocks.split(",") if s.strip()]
        watchlist.STOCK_TO_ADD = []
        watchlist.STOCK_TO_REMOVE = []
        
    elif action == "MODIFY":
        add_stocks = input("Enter stocks to ADD separated by commas (or press Enter to skip): ").strip().upper()
        remove_stocks = input("Enter stocks to REMOVE separated by commas (or press Enter to skip): ").strip().upper()
        
        watchlist.STOCK_LIST = []
        watchlist.STOCK_TO_ADD = [s.strip() for s in add_stocks.split(",") if s.strip()] if add_stocks else []
        watchlist.STOCK_TO_REMOVE = [s.strip() for s in remove_stocks.split(",") if s.strip()] if remove_stocks else []

    # Execute the module
    print("\nExecuting Watchlist modification...")
    watchlist.main()


def handle_analysis():
    print_header("LLM Analysis & Auto-Trade")
    
    save_opt = input("Do you want to save the LLM prompts and responses to file? (y/n): ").strip().lower()
    auto_opt = input("Do you want the bot to AUTO-TRADE based on the LLM response? (y/n): ").strip().lower()

    # Update main.py global variables
    analysis_main.SAVE_OUTPUTS = (save_opt == 'y')
    analysis_main.AUTO_TRADE = (auto_opt == 'y')

    # Execute the module
    print(f"\nExecuting Pipeline (Auto-Trade: {analysis_main.AUTO_TRADE}, Save: {analysis_main.SAVE_OUTPUTS})...")
    analysis_main.main()


def handle_trade():
    print_header("Manual Trade Execution")
    print("Enter your orders one by one.")
    print("Format: [SYMBOL] [BUY/SELL] [AMT/SHR] [AMOUNT]")
    print("Example: AAPL BUY AMT 10000")
    print("Type 'DONE' when you are finished entering orders.")
    print("-" * 50)

    orders = []
    while True:
        order = input("Order > ").strip().upper()
        if order == "DONE":
            break
        if order:
            orders.append(order)

    if not orders:
        print("No orders entered. Returning to main menu.")
        return

    # Update trade.py global variable
    trade.ORDERS = orders

    # Execute the module
    print("\nDispatching Manual Trades...")
    trade.main()


def handle_portfolio():
    print_header("Portfolio Viewer")
    
    save_opt = input("Do you want to save your portfolio to a YAML file? (y/n): ").strip().lower()
    
    # Update portfolio.py global variable
    portfolio.SAVE_TO_FILE = (save_opt == 'y')

    # Execute the module
    print("\nFetching Portfolio...")
    portfolio.main()


def main_menu():
    while True:
        print_header("Algorithmic Trading Command Line Interface")
        print("1. Manage Watchlists")
        print("2. Run LLM Analysis & Auto-Trade")
        print("3. Execute Manual Trades")
        print("4. View Portfolio")
        print("5. Exit")
        print("-" * 50)
        
        choice = input("Select an option (1-5): ").strip()
        
        if choice == '1':
            handle_watchlist()
        elif choice == '2':
            handle_analysis()
        elif choice == '3':
            handle_trade()
        elif choice == '4':
            handle_portfolio()
        elif choice == '5':
            print("\nExiting. Goodbye!")
            sys.exit(0)
        else:
            print("\nInvalid choice. Please enter a number between 1 and 5.")


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user. Exiting.")
        sys.exit(0)