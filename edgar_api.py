# edgar_api.py

import requests
import json
import os

HEADERS = {
    "User-Agent": "Arturo N. Regueira arturoMcgillicutty@outlook.com",  # Use a legit email per SEC rules
    "Accept-Encoding": "gzip, deflate"
}

def get_company_submissions(cik_or_ticker: str):
    """Query EDGAR's company submissions endpoint."""
    base_url = "https://data.sec.gov/submissions/"
    cik = cik_or_ticker.zfill(10) if cik_or_ticker.isdigit() else get_cik_from_ticker(cik_or_ticker)
    url = f"{base_url}CIK{cik}.json"
    print(url)
    print()
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    print(f"GET {url} → {response.status_code}")
    return response.json()

def get_cik_from_ticker(ticker: str):
    """Get the CIK for a given ticker symbol."""
    url = f"https://www.sec.gov/files/company_tickers.json"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    ticker_map = response.json()
    for entry in ticker_map.values():
        if entry['ticker'].lower() == ticker.lower():
            return str(entry['cik_str']).zfill(10)
    raise ValueError(f"Ticker '{ticker}' not found.")

def save_JSON(file,filename):
    folder = "data"
    os.makedirs(folder,exist_ok=True)
    filepath = os.path.join(folder,filename)

    with open(filepath,"w") as f:
        json.dump(file,f,indent = 5)

