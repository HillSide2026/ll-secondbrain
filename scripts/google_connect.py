import os
from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow

load_dotenv()

CLIENT_PATH = os.getenv("GOOGLE_OAUTH_CLIENT_PATH", "config/google_oauth_client.json")
TOKEN_PATH = os.getenv("GOOGLE_OAUTH_TOKEN_PATH", "config/google_oauth_tokens.json")

SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/spreadsheets",
]

def main():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_PATH, SCOPES)
    creds = flow.run_local_server(port=0, prompt="consent", access_type="offline")

    with open(TOKEN_PATH, "w") as f:
        f.write(creds.to_json())

    print(f"Saved tokens to: {TOKEN_PATH}")
    if getattr(creds, "refresh_token", None):
        print("✅ refresh_token granted.")
    else:
        print("⚠️ No refresh_token. Revoke app access and retry.")

if __name__ == "__main__":
    main()
