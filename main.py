# main.py

from edgar_api import get_company_submissions, save_JSON


if __name__ == "__main__":
    ticker = "AAPL"  # Apple Inc.
    data = get_company_submissions(ticker)
    
    save_JSON(data,f"{ticker}-filings.json")
