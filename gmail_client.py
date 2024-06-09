from imap_tools import MailBox, A
import smtplib
import json
import base64
import threading
import requests
import os
# from dotenv import load_dotenv
from sqlite_client import SQLiteClient
import eel
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import config


db = SQLiteClient()
eel.init('client/src/api', allowed_extensions=['.ts'])

class GmailClient:
    """
    Gmail Client interacts with google apis to authenticate user,
    logout user, and fetch and send emails using IMAP/SMTP
    """
    def __init__(self):
        # create if to grab saved client data from pickle file
        # if client exists in pickle file:
            # self.user = user.from_file
        # else:
        self.user: str = None
        self.access_token: str = None
        self.refresh_token: str = None
        # eel.getEmails()
        # threading.Timer(10, self.new_thread).start()
    
    def auth(self, code: str):
        """
        Authenticates gmail user using OAuth 2.0.
        :param code: response code from google oauth server to fetch access token
        :return: authentication Json
        """
        data = {
            'client_id': config.GMAIL_CLIENT_ID,
            'client_secret': config.GMAIL_CLIENT_SECRET,
            'redirect_uri': 'http://localhost:3000/auth', # Windows
            # 'redirect_uri': 'http://localhost:9000', # Mac
            'grant_type': 'authorization_code',
            'code': code}
        
        print('CODE: ', code)
    
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
        token_requests = requests.post('https://accounts.google.com/o/oauth2/token', data=data, headers=headers)
        # load data to user json 
        user_info_json = json.loads(token_requests.text)
        print("USER INFO JSON: ", user_info_json)
        get_user_email_url = f'''https://www.googleapis.com/oauth2/v1/userinfo?access_token={user_info_json['access_token']}'''
        get_user_email = requests.get(get_user_email_url, headers={'Content-Type': 'application/json; charset=utf-8'})
        user_info_json.update(json.loads(get_user_email.text))

        self.user = user_info_json['email']
        self.access_token = user_info_json['access_token']
        self.refresh_token = user_info_json['refresh_token']
        # start thread to continously load new emails
        threading.Timer(0, self.new_thread).start()
        return {'Authenticated': 'True'}
        
    def fetch_mailbox(self):
        """
        Use IMAP protocol to fetch emails from server.
        Stores email in SQLite DB and updates client.
        """
        mailbox = MailBox('imap.gmail.com', 993).xoauth2(self.user, self.access_token, 'Inbox')
        # instead of while true, set max at 100: max 1000 fetched emails
        for i in range(20):
            # fetch 5 at a time
            BULK_LIMIT = 10
            for msg in mailbox.fetch(limit=slice(i*BULK_LIMIT, (i*BULK_LIMIT) + BULK_LIMIT), reverse=True, bulk=True, mark_seen=False):
                uniquekey = f'{self.user}{msg.uid}'
                seen = 'False'
                flagged = 'False'
                print(msg.flags)
                if 'Seen' in str(msg.flags):
                    seen = 'True'
                if 'Flagged' in str(msg.flags):
                    flagged = 'True'
                    
                email = msg.html
                if email == '':
                    print("MESSSAGE NO HTML: ", email)
                    email = msg.text

                result = db.store_email(uniquekey, 'gmail', seen, flagged, msg.uid, msg.subject, msg.from_, str(msg.to), str(msg.date), email)
                if result == 'Done':
                    print("DONE")
                    eel.getEmailsPortal()
                    return

    def send_email(self, to: str, body: str, subject: str):
        """
        Sends email using SMTP with OAuth 2.0
        :return: 'Invalid Recipients' string if send address fails
        :return: 'Success' string if success
        """
        print(f"SENDING EMAILL: to:{to}, email:{self.user}, subject:{subject}")
        
        smtp_conn = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_conn.starttls()
        auth_string = f'user={self.user}\x01auth=Bearer {self.access_token}\x01\x01'
        xoauth2 = base64.b64encode(auth_string.encode('utf-8'))
        smtp_conn.docmd('AUTH', 'XOAUTH2 ' + xoauth2.decode('utf-8'))
        
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        html = MIMEText(body, 'html')
        msg.attach(html)

        try:
            print("SENDING EMAIL")
            smtp_conn.sendmail(self.user, to, msg.as_string())
        except smtplib.SMTPRecipientsRefused as e:
            print('SMTPRecipientsRefused: ', e)
            return 'Invalid Recipients'
        except Exception as e:
            print("Another Exception", e)
            return 'Failure'
        smtp_conn.quit()
        print("Message sent!")
        return 'Success'
    
    # TODO
    def new_thread(self):
        if self.user != None:
            self.fetch_mailbox()
        threading.Timer(60, self.new_thread).start()

    def logout(self):
        """
        Revokes access token forcing user to sign in again.
        """
        # curl -H "Content-type:application/x-www-form-urlencoded" https://accounts.google.com/o/oauth2/revoke?token=
        url = f'https://accounts.google.com/o/oauth2/revoke?token={self.refresh_token}'
        headers = {'content-type': 'application/x-www-form-urlencoded', 'Accept-Charset': 'UTF-8'}
        request = requests.get(url, headers=headers)
        print("REQUEST TEXT: ", request.text)
        if json.loads(request.text) == '\\{\\}':
            print("Logged Out")
        else:
            print("Logout Error")

    # NEED TO CONFIRM WORKING
    def refresh_access_token(self):
        """
        Refreshes access token using refresh token when access token expires.
        """
        print("Refreshing Token...")
        data = {'client_id': config.GMAIL_CLIENT_ID,
            'client_secret': config.GMAIL_CLIENT_SECRET,
            'refresh_token': self.refresh_token,
            'grant_type': 'refresh_token'}
        
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
        token_requests = requests.post('https://accounts.google.com/o/oauth2/token', data=data, headers=headers)
        # load data to new token json 
        new_token_json = json.loads(token_requests.text)
        self.access_token = new_token_json['access_token']