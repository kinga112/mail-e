from imap_tools import MailBox
import smtplib
import json
import base64
import time
import threading
import requests
import os
import atexit
from dotenv import load_dotenv
from sqlite_client import SQLiteClient
# from sql_client import SQLiteClient

db = SQLiteClient()

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
        threading.Timer(10, self.new_thread).start()
    
    def auth(self, code: str):
        """
        Authenticates gmail user using OAuth 2.0.
        :param code: response code from google oauth server to fetch access token
        :return: authentication Json
        """
        load_dotenv()
        data = {'client_id': os.getenv('GMAIL_CLIENT_ID'),
            'client_secret': os.getenv('GMAIL_CLIENT_SECRET'),
            'redirect_uri': 'http://localhost:3000/gmail/auth',
            'grant_type': 'authorization_code',
            'code': code}
    
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
        token_requests = requests.post('https://accounts.google.com/o/oauth2/token', data=data, headers=headers)
        # load data to user json 
        user_info_json = json.loads(token_requests.text)
        get_user_email_url = f'''https://www.googleapis.com/oauth2/v1/userinfo?access_token={user_info_json['access_token']}'''
        get_user_email = requests.get(get_user_email_url, headers={'Content-Type': 'application/json; charset=utf-8'})
        user_info_json.update(json.loads(get_user_email.text))

        self.user = user_info_json['email']
        self.access_token = user_info_json['access_token']
        self.refresh_token = user_info_json['refresh_token']

        return {'Authenticated': 'True'}
        
    def fetch_mailbox(self):
        print("FETCHING MAILBOX")
        mailbox = MailBox('imap.gmail.com', 993).xoauth2(self.user, self.access_token, 'Inbox')

        # LOOK INTO THIS: flags=('\\Unmarked', '\\HasChildren')
        # for f in mailbox.folder.list('[Gmail]'):
            # print(f)  # FolderInfo(name='INBOX|cats', delim='|', flags=('\\Unmarked', '\\HasChildren'))
        # emails = []

        ## TEST THIS: 
        #####
        #from imap_tools import MailBox, A
        #
        # waiting for updates 60 sec, print unseen immediately if any update
        #with MailBox('imap.my.moon').login('acc', 'pwd', 'INBOX') as mailbox:
        #    responses = mailbox.idle.wait(timeout=60)
        #    if responses:
        #        for msg in mailbox.fetch(A(seen=False)):
        #            print(msg.date, msg.subject)
        #    else:
        #        print('no updates in 60 sec')
        #
        ####

        # instead of while true, set max at 100: max 500 fetched emails
        for i in range(100):
            # fetch 5 at a time
            for msg in mailbox.fetch(limit=slice(i*5,(i*5)+5), reverse=True, bulk=True, mark_seen=False):
                uniquekey = f'{self.user}{msg.uid}'
                seen = 'False'
                flagged = 'False'
                if '\\Seen' in msg.flags:
                    print("SEEN IS TRUE")
                    seen = 'True'
                if '\\Flagged' in msg.flags:
                    print("FLAGGED IS TRUE")
                    flagged = 'True'

                result = db.store_email(uniquekey, 'gmail', seen, flagged, msg.uid, msg.subject, msg.from_, str(msg.to), msg.date_str, msg.html)
                if result == 'Done':
                    return

    def send_email(self, to: str, subject: str, body: str):
        """
        Sends email using SMTP with OAuth 2.0
        :return: 'Invalid Recipients' string if send address fails
        :return: 'Success' string if success
        """
        print(f"SENDING EMAILL: to:{to}, email:{self.user}, subject:{subject}")
        
        smtp_conn = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_conn.starttls()
        auth_string = f"user={self.user}\x01auth=Bearer {self.access_token}\x01\x01"
        xoauth2 = base64.b64encode(auth_string.encode('utf-8'))
        smtp_conn.docmd('AUTH', 'XOAUTH2 ' + xoauth2.decode('utf-8'))
        
        # header = 'Subject: ' + subject + '\n'
        # check if this works
        header = f'Subject: {subject}\n'
        header += 'Content-Type: text/html; charset=UTF-8\n'
        msg = header + body
        try:
            print("SENDING EMAIL")
            smtp_conn.sendmail(self.user, to, msg)
        except smtplib.SMTPRecipientsRefused as e:
            print('CAUGHT YEAHHHHH Invalid Recipients : ', e)
            return 'Invalid Recipients'
        except Exception as e:
            print("ANOTHER EXCEPTION", e)
        smtp_conn.quit()
        print("Message sent!")
        return 'Success'
    
    # TODO
    def new_thread(self):
        print("THIS IS THE THREAD FUNCTION")
        if self.user != None:
            self.fetch_mailbox()
        threading.Timer(60, self.new_thread).start()
        # atexit.register(threading.Timer.join())

    def logout(self):
        """
        Revokes access token forcing user to sign in again.
        """
        print("GMAIL LOGOUT")
        # curl -H "Content-type:application/x-www-form-urlencoded" https://accounts.google.com/o/oauth2/revoke?token=
        url = f'https://accounts.google.com/o/oauth2/revoke?token={self.refresh_token}'
        headers = {'content-type': 'application/x-www-form-urlencoded', 'Accept-Charset': 'UTF-8'}
        request = requests.get(url, headers=headers)
        print("REQUEST TEXT: ", request.text)
        if json.loads(request.text) == '\\{\\}':
            print("LOGGED OUT")
        else:
            print("LOGOUT ERROR?")

    # NEED TO CONFIRM WORKING
    def refresh_access_token(self):
        """
        Refreshes access token using refresh token when access token expires.
        """
        print("REFRESING TOKEN")
        load_dotenv()

        data = {'client_id': os.getenv('GMAIL_CLIENT_ID'),
            'client_secret': os.getenv('GMAIL_CLIENT_SECRET'),
            'refresh_token': self.refresh_token,
            'grant_type': 'refresh_token'}
        
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
        token_requests = requests.post('https://accounts.google.com/o/oauth2/token', data=data, headers=headers)
        # load data to new token json 
        new_token_json = json.loads(token_requests.text)
        self.access_token = new_token_json['access_token']