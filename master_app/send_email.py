import os
import base64
import pickle
import json
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
TOKEN_FILEPATH = BASE_DIR / 'master_app'  / 'token.pickle'

# Scopes required for sending emails
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# Function to authenticate and build the Gmail service
def authenticate_gmail():
    # print(BASE_DIR / 'master_app' )
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, created automatically when the authorization flow completes.
    if os.path.exists(TOKEN_FILEPATH):
        with open(TOKEN_FILEPATH, 'rb') as token:
            creds = pickle.load(token)
    
    # If no valid credentials, ask the user to log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILEPATH, 'wb') as token:
            pickle.dump(creds, token)
    
    # Build the Gmail service
    service = build('gmail', 'v1', credentials=creds)
    return service

# Function to create an email message
def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

# Function to send an email
def send_email(service, user_id, message):
    try:
        message = service.users().messages().send(userId=user_id, body=message).execute()
        print(f"Message sent! Message ID: {message['id']}")
    except Exception as e:
        print(f"An error occurred: {e}")

def email_send(data):
    # Authenticate and create the Gmail API service
    service = authenticate_gmail()

    # Email details
    sender = 'sharesecure55@gmail.com'
    to = 'sharesecure55@gmail.com'
    subject = 'File Uploaded'
    message_text = data

    # Create the email message
    message = create_message(sender, to, subject, message_text)

    # Send the email
    send_email(service, 'me', message)
