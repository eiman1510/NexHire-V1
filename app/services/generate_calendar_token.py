from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/calendar"]
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_FILE = BASE_DIR / "google_calendar_secret.json"
TOKEN_FILE = BASE_DIR / "token.json"

flow = InstalledAppFlow.from_client_secrets_file(str(SECRET_FILE), SCOPES)

creds = flow.run_local_server(port=0)

with open(TOKEN_FILE, "w") as token:
    token.write(creds.to_json())

print("Token generated successfully")
