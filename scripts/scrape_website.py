"""
Official Website Scraper for P. R. Pote Patil College of Engineering & Management (PRPCEM), Amravati.
Fetches authoritative pages from:
  - https://prpotepatilengg.ac.in/
  - https://academics.prpotepatilengg.ac.in/

Saves raw content into data/raw/ directory.
Safeguards existing data in case of connection failure.
"""

import os
import json
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
SOURCES_FILE = os.path.join(BASE_DIR, "data", "sources.json")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) PotentialAI-Scraper/1.0"
}

ALLOWED_DOMAINS = ["prpotepatilengg.ac.in", "academics.prpotepatilengg.ac.in"]

def is_allowed_url(url: str) -> bool:
    return any(domain in url for domain in ALLOWED_DOMAINS)

def scrape_official_websites():
    os.makedirs(RAW_DIR, exist_ok=True)
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting PRPCEM Official Website Scraper...")

    scraped_data = {
        "metadata": {
            "retrieved_at": datetime.now().isoformat(),
            "scraper_version": "1.0",
            "domains": ALLOWED_DOMAINS
        },
        "pages": {},
        "academic_nodes": {},
        "bundles": {}
    }

    # 1. Main College Portal & Angular Bundles
    main_url = "https://prpotepatilengg.ac.in/"
    try:
        print(f"Fetching main website: {main_url}")
        res = requests.get(main_url, headers=HEADERS, timeout=15)
        if res.status_code == 200:
            scraped_data["pages"]["main_home"] = {
                "url": main_url,
                "status": 200,
                "html": res.text,
                "retrieved_at": datetime.now().isoformat()
            }
            print("Successfully fetched main homepage.")
            
            # Fetch Angular main bundle for client-side data
            bundle_url = "https://prpotepatilengg.ac.in/main.bd38d45b9608e2b8.js"
            print(f"Fetching Angular main bundle: {bundle_url}")
            res_bundle = requests.get(bundle_url, headers=HEADERS, timeout=15)
            if res_bundle.status_code == 200:
                scraped_data["bundles"]["main_bundle"] = {
                    "url": bundle_url,
                    "status": 200,
                    "text": res_bundle.text,
                    "retrieved_at": datetime.now().isoformat()
                }
                print(f"Fetched main bundle ({len(res_bundle.text)} characters).")
        else:
            print(f"Main website returned HTTP status: {res.status_code}")
    except Exception as e:
        print(f"[WARNING] Could not fetch main site: {e}. Preserving existing knowledge.")

    # 2. Academics Portal & Nodes
    academics_url = "https://academics.prpotepatilengg.ac.in/"
    try:
        print(f"Fetching academics portal: {academics_url}")
        res_acad = requests.get(academics_url, headers=HEADERS, timeout=15)
        if res_acad.status_code == 200:
            scraped_data["pages"]["academics_home"] = {
                "url": academics_url,
                "status": 200,
                "html": res_acad.text,
                "retrieved_at": datetime.now().isoformat()
            }
            print("Successfully fetched academics homepage.")

            # Crawl academic notices & syllabus pages
            for page in range(0, 5):
                page_url = f"https://academics.prpotepatilengg.ac.in/?page={page}"
                try:
                    p_res = requests.get(page_url, headers=HEADERS, timeout=10)
                    if p_res.status_code == 200:
                        soup = BeautifulSoup(p_res.text, "html.parser")
                        for a in soup.find_all("a"):
                            href = a.get("href", "")
                            text = a.get_text(strip=True)
                            if "/node/" in href and text and href not in scraped_data["academic_nodes"]:
                                node_full_url = f"https://academics.prpotepatilengg.ac.in{href}"
                                scraped_data["academic_nodes"][href] = {
                                    "title": text,
                                    "url": node_full_url,
                                    "category": "scheme_or_notice",
                                    "academic_year": "2026-27" if "2026" in text else "2025-26"
                                }
                except Exception as pe:
                    print(f"Warning fetching page {page}: {pe}")
            print(f"Discovered {len(scraped_data['academic_nodes'])} academic nodes.")
    except Exception as e:
        print(f"[WARNING] Could not fetch academics portal: {e}. Preserving existing knowledge.")

    raw_file = os.path.join(RAW_DIR, "raw_scraped_data.json")
    # Only overwrite if we got valid data or file does not exist
    if scraped_data["pages"] or not os.path.exists(raw_file):
        with open(raw_file, "w", encoding="utf-8") as f:
            json.dump(scraped_data, f, indent=2, ensure_ascii=False)
        print(f"Saved raw scraped data to {raw_file}")
    else:
        print("Scraper encountered errors; retained previous raw data.")

if __name__ == "__main__":
    scrape_official_websites()
