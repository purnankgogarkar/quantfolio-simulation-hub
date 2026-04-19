import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def build_stock_universe():

    print("Downloading NSE stock list...")

    try:
        nse_url = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"
        nse = pd.read_csv(nse_url)
        nse = nse[["SYMBOL", "NAME OF COMPANY"]]
        nse.columns = ["Ticker", "Name"]
        nse["Exchange"] = "NSE"
        nse["Ticker"] = nse["Ticker"] + ".NS"
        print(f"NSE stocks loaded: {len(nse)}")
    except Exception as e:
        print(f"Error loading NSE data: {e}")
        nse = pd.DataFrame(columns=["Ticker", "Name", "Exchange"])

    print("Downloading BSE stock list...")

    try:
        bse_url = "https://api.bseindia.com/BseIndiaAPI/api/ListofScripData/w"
        
        # Add headers and retry strategy to handle 403 error
        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = session.get(bse_url, headers=headers, timeout=10)
        response.raise_for_status()
        bse = pd.DataFrame(response.json())
        
        if len(bse) > 0:
            bse = bse[["Security Code", "Security Id", "Security Name"]]
            bse.columns = ["Code", "Ticker", "Name"]
            bse["Exchange"] = "BSE"
            bse["Ticker"] = bse["Ticker"] + ".BO"
            bse = bse[["Ticker", "Name", "Exchange"]]
            print(f"BSE stocks loaded: {len(bse)}")
        else:
            bse = pd.DataFrame(columns=["Ticker", "Name", "Exchange"])
            
    except Exception as e:
        print(f"Error loading BSE data: {e}. Using NSE data only.")
        bse = pd.DataFrame(columns=["Ticker", "Name", "Exchange"])

    nse = nse[["Ticker", "Name", "Exchange"]]

    universe = pd.concat([nse, bse], ignore_index=True)
    universe = universe.drop_duplicates(subset="Ticker")

    # Create data directory if it doesn't exist
    import os
    os.makedirs("data", exist_ok=True)

    universe.to_csv("data/stock_universe.csv", index=False)

    print("Stock universe saved")
    print("Total stocks:", len(universe))


if __name__ == "__main__":
    build_stock_universe()