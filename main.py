# main.py

import  edgar_api #functiones receptae ex edgar_api.py
import multo_datum
import requests
import time
import os


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
        for i, m in enumerate(matches, start=1):
            print(f"• {m['filingDate']} - {form_type} - {m['url']}")

            try:
                doc_url = edgar_api.get_url(m,form_type)
                print(f"Primary document: {doc_url}")
                time.sleep(1.5)
                response = requests.get(doc_url, headers= multo_datum.HEADERS)
                
                response.raise_for_status()

                save_folder = "filings"

                os.makedirs(save_folder, exist_ok = True) 
                filename = f"{ticker}_{form_type}_{m['filingDate']}.html"

                filepath = os.path.join(save_folder,filename)

                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(response.text)

                print(f"Saved HTML to: {filepath}\n")

            except Exception as e:
                print(f" ⚠️ Error downloading primary document: {e}\n")


    except ValueError as e:
        print("reiectus quia",e)

if __name__ == "__main__":
    main()
