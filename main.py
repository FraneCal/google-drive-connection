from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# OAuth scope that allows uploading and managing your own Drive files
SCOPES = ["https://www.googleapis.com/auth/drive.file"]

# The folder you want to upload into (the one you shared earlier)
PARENT_FOLDER_ID = "1myZCiTa_pXQmb9DTw1si4ml2zF0xl2Xp"

def main():
    # Step 1: Run the OAuth flow (opens browser window once)
    flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
    creds = flow.run_local_server(port=0)

    # Step 2: Build the Drive API service
    service = build("drive", "v3", credentials=creds)

    # Step 3: Prepare file metadata and content
    file_metadata = {
        "name": "hello.txt",
        "parents": [PARENT_FOLDER_ID],
    }
    media = MediaFileUpload("requirements.txt", resumable=True)

    # Step 4: Upload the file
    file = (
        service.files()
        .create(body=file_metadata, media_body=media, fields="id, name, parents")
        .execute()
    )

    print(f"✅ Uploaded: {file.get('name')} (ID: {file.get('id')})")

if __name__ == "__main__":
    main()
