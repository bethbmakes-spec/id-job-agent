import os
from dotenv import load_dotenv
from scraper import build_digest
from mailer import send_digest

load_dotenv()

def main():
    api_key = os.environ.get("GOOGLE_API_KEY")
    cse_id = os.environ.get("GOOGLE_CSE_ID")
    rows, csv_path = build_digest(api_key, cse_id)
    print(f"Found {len(rows)} qualifying postings -> {csv_path}")
    send_digest(rows, csv_path)

if __name__ == "__main__":
    main()
