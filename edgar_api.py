# edgar_api.py 
# Applicatio Programmationis Interfaciei

import requests
import json
import os
import multo_datum
import re
from bs4 import BeautifulSoup

HEADERS = multo_datum.HEADERS

def get_company_submissions(cik_or_ticker: str):
    """Accipe punctum finale submissionum societatis EDGAR."""
    base_url = "https://data.sec.gov/submissions/"
    #cik = cik_or_ticker.zfill(10) if cik_or_ticker.isdigit() else get_cik_from_ticker(cik_or_ticker)
    if cik_or_ticker.isdigit():
        cik = cik_or_ticker.zfill(10)
    else:
        cik = get_cik_from_ticker(cik_or_ticker)
    url = f"{base_url}CIK{cik}.json"
    print(url)
    print()
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    print(f"GET {url} --> {response.status_code}")
    return response.json()

def get_cik_from_ticker(ticker: str):
    """CIK pro dato symbolo ticker accipe."""
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


def get_filings(data,form_type,count=1):
     """Excerpe unam vel plures actas formularii certi generis ex *company submissions JSON* quod redditur a `get_company_submissions`.

    Argumenta:
    data (dict): Objectum JSON redditum a `get_company_submissions()`
    form_type (str): e.g., "10-K", "8-K"
    count (int): Quot recensiones recentes reddendae sint

    Reddit:
    Index dictorum cum metadata actarum"""
     recent_forms = data["filings"]["recent"]
     matches = []

     for i, form in enumerate(recent_forms["form"]):
        if form.upper() == form_type.upper():
            accessionNumber = recent_forms["accessionNumber"][i].replace("-","")
            filing = {
                "accessionNumber" : accessionNumber,
                "filingDate" : recent_forms["filingDate"][i],
                "primaryDocument" : recent_forms["primaryDocument"][i],
                "cik" : data["cik"].lstrip("0"),
                "url" : f"https://www.sec.gov/Archives/edgar/data/{data['cik'].lstrip('0')}/{accessionNumber}/{accessionNumber}-index.htm"
            }
            matches.append(filing)

            if len(matches) >= count:
                break
     if not matches:
         raise ValueError(f"Non {form_type} inscriptiones in datis inventae.")
     #print(matches)
     return matches

def get_url(fil_match, form_type):
    #Iurl = fil_match["url"]

    cik = str(fil_match["cik"]).lstrip("0")
    acc_no_nodash = fil_match["accessionNumber"].replace("-", "")
    primaryDocument = fil_match.get("primaryDocument")

    if not primaryDocument:
        raise ValueError(f"primary document missing for {fil_match["filingDate"]}")

    Iurl = f"https://www.sec.gov/Archives/edgar/data/{cik}/{acc_no_nodash}/{primaryDocument}"

    return Iurl
    #resq = requests.get(Iurl, headers = HEADERS)
    #resq.raise_for_status()

    #sopa = BeautifulSoup(resq.content, "html.parser")
    #table = sopa.find("table", {"summary": "Document Format Files"})

    #for row in table.find_all("tr")[1:]:  # "[1:]" ad praeterire inutiles
        #cols = row.find_all("td")
        #description = cols[1].get_text(strip=True).lower()
        #href = cols[2].find("a")["href"]

        #if form_type in description or f"form {form_type}" in description or fil_match['primaryDocument'].lower() in href.lower():
            #return f"https://www.sec.gov{href}"
        
    #raise Exception(f"{form_type} not found")





        
