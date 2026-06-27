import logging
import os

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from googleapiclient.discovery import build

logger = logging.getLogger(__name__)

SCOPES = ['https://www.googleapis.com/auth/calendar']
TIME_ZONE = "Asia/Kolkata"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLIENT_SECRET = os.path.join(BASE_DIR, "client_secret.json")
TOKEN = os.path.join(BASE_DIR, "token.json")


def get_service():
    creds = None

    if os.path.exists(TOKEN):
        creds = Credentials.from_authorized_user_file(
            TOKEN,
            SCOPES,
        )

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET,
                SCOPES,
            )
            creds = flow.run_local_server(port=0)

        with open(TOKEN, "w") as token:
            token.write(creds.to_json())

    return build("calendar", "v3", credentials=creds)


def create_event(doctor, patient, start, end):
    service = get_service()

    event = {
        "summary": f"Appointment with Dr. {doctor}",
        "description": f"Patient: {patient}",
        "start": {
            "dateTime": start.isoformat(),
            "timeZone": TIME_ZONE,
        },
        "end": {
            "dateTime": end.isoformat(),
            "timeZone": TIME_ZONE,
        },
    }

    event = service.events().insert(
        calendarId="primary",
        body=event,
    ).execute()

    logger.info("Google Calendar Event Created: %s", event.get("htmlLink"))
