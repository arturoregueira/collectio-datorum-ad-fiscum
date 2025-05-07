# main.py

import  edgar_api #functiones receptae ex edgar_api.py


def main():
    ticker = input("Praebe ticker ").upper()
    form_type = input("Praebe forma ").upper()
    count = int(input("quantitas "))
    
    print(f"Recuperatio inscriptionum pro {ticker}...")
    data = edgar_api.get_company_submissions(ticker)
    edgar_api.save_JSON(data,f"{ticker}--filings.json")

    print(f" Filtratio usque ad {count} '{form_type}' formae...")

    try:
        matches = edgar_api.get_filings(data,form_type=form_type,count=count )
        for m in matches:
            print(f"� {m['filingDate']} - {form_type} - {m['url']}")
    except ValueError as e:
        print("reiectus quia",e)

if __name__ == "__main__":
    main()
