from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from bs4 import BeautifulSoup
import requests
import json
import os

# ==== CONFIGURATION ====
SCOPES = ["https://www.googleapis.com/auth/drive.file"]
PARENT_FOLDER_ID = "1myZCiTa_pXQmb9DTw1si4ml2zF0xl2Xp"

FILENAME = "scraped_data"

URL = "https://hr.wikipedia.org/wiki/Hrvatska"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}


# ==== SCRAPER FUNCTION ====
def scraper():
    """Scrape data from Wikipedia (you can modify what to extract)."""
    response = requests.get(URL, headers=HEADERS)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Example: extract the page title
    title = soup.find("h1", class_="firstHeading").get_text(strip=True)

    # Example: extract the first paragraph text
    first_paragraph = soup.find("p").get_text(strip=True)

    # Return structured data (easy to expand later)
    return {
        "url": URL,
        "title": title,
        "first_paragraph": first_paragraph
    }


# ==== SAVE TO JSON FUNCTION ====
def save_to_json(data, filename=f"{FILENAME}.json"):
    """Save scraped data to a JSON file."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return filename


# ==== GOOGLE DRIVE UPLOAD FUNCTION ====
def upload_to_drive(file_path, creds):
    """Upload file to Google Drive."""
    service = build("drive", "v3", credentials=creds)

    file_metadata = {
        "name": os.path.basename(file_path),
        "parents": [PARENT_FOLDER_ID],
    }

    media = MediaFileUpload(file_path, resumable=True)

    file = (
        service.files()
        .create(body=file_metadata, media_body=media, fields="id, name, parents")
        .execute()
    )

    print(f"✅ Uploaded: {file.get('name')} (ID: {file.get('id')})")


# ==== MAIN FUNCTION ====
def main():
    # Step 1: Run OAuth flow
    flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
    creds = flow.run_local_server(port=0)

    # Step 2: Scrape data
    scraped_data = scraper()
    print(f"🕸️ Scraped title: {scraped_data['title']}")

    # Step 3: Save to file
    output_file = save_to_json(scraped_data)
    print(f"💾 Data saved locally as {output_file}")

    # Step 4: Upload to Google Drive
    upload_to_drive(output_file, creds)


# ==== RUN ====
if __name__ == "__main__":
    main()
