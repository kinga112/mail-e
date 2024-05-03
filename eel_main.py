import base64
import json
from gmail_client import GmailClient
from sqlite_client import SQLiteClient
from yahoo_client import YahooClient
from imap_tools import MailBox
import smtplib
import sqlite3
import eel
import socket

gmail_client = GmailClient()
yahoo_client = YahooClient()

@eel.expose
def authorize(email_service: str):
    """
    Decodes auth code from socket.
    Determines Oauth2 route from email_service ('gmail', 'outlook', 'yahoo').
    """
    # create websocket to listen for incoming code
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind(('', 5000))
    except:
        print('Bind failed. Error')
        return {'Authenticated': 'False'}

    ###
    # 1 here means that 1 connection is kept waiting if the server is busy 
    # and if a 2nd socket tries to connect then the connection is refused.
    ###
    s.listen(1)
    code = ''

    while True:
        conn, addr = s.accept()
        url_bytes = conn.recv(4096).decode("utf-8")
        code = url_bytes.split('code=')[1].split('&scope=')[0].replace('%2F', '/')
        break

    match email_service:
        case 'gmail':
            success = gmail_client.auth(code)
        case 'outlook':
            print("OUTLOOK")
        case 'yahoo':
            success = yahoo_client.auth(code)

    return success

# REMOVE
@eel.expose
def get_emails(folder: str, start: int, end: int):
    # email_client = EmailClient(email, access_token)
    # return email_client.get_email(folder, start, end)
    # print(f"GET EMAILS: folder:{folder} email:{email}, a_t:{access_token}")
    if folder != 'Inbox':
        folder = f'[Gmail]/{folder}'
        

    print(f"GMAIL USER: {gmail_client.user} GMAIL TOKEN: {gmail_client.access_token}")
    mailbox = MailBox('imap.gmail.com', 993).xoauth2(gmail_client.user, gmail_client.access_token, folder)
    # for f in mailbox.folder.list('[Gmail]'):
        # print(f)  # FolderInfo(name='INBOX|cats', delim='|', flags=('\\Unmarked', '\\HasChildren'))
    emails = []
    for i in range(5):
        print("I: ", i)
        # for msg in mailbox.fetch(limit=slice(start,end), reverse=True, bulk=True, mark_seen=False):
        for msg in mailbox.fetch(limit=slice(i*5,(i*5)+5), reverse=True, bulk=True, mark_seen=False):
            print('MESSAGE: ', msg.flags)
            email = {'uid': msg.uid,
                    'subject': msg.subject,
                    'from': msg.from_,
                    'to': msg.to,
                    'date': msg.date,
                    'attachments': msg.attachments,
                    'html': msg.html}
            # email = {'uid': msg.uid, 'subject': msg.subject, 'from': msg.from_, 'to': msg.to, 'date': msg.date}
            # store_email(folder, msg.uid, msg.subject, msg.from_, msg.to, msg.date_str, msg.html)
            # email = {'from': msg.from_, 'to': msg.to, 'date': msg.date}
            # print(msg.from_)
            # break
            # print(email)
            # print(json.dumps(email, sort_keys=True, default=str))
            # emails[index] = json.dumps(email, sort_keys=True, default=str)
            # emails.append(json.dumps(email, sort_keys=True, default=str))
            emails.append(email)
        # print("EMAILS: ", emails)
        # print("done")
        # cache(folder, emails)
    return emails


# REMOVE
@eel.expose
def send_email(email, access_token, to, body, subject):
    print(f"SENDING EMAILL: to:{to}, email:{email}, subject:{subject}")
    smtp_conn = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_conn.starttls()
    auth_string = f"user={email}\x01auth=Bearer {access_token}\x01\x01"
    xoauth2 = base64.b64encode(auth_string.encode('utf-8'))
    smtp_conn.docmd('AUTH', 'XOAUTH2 ' + xoauth2.decode('utf-8'))
    
    header = 'Subject: ' + subject + '\n'
    header += 'Content-Type: text/html; charset=UTF-8\n'
    msg = header + body
    try:
        print("SEND MAIN: ", smtp_conn.sendmail(email, to, msg))
    except smtplib.SMTPRecipientsRefused as e:
        print('CAUGHT YEAHHHHH Invalid Recipients : ', e)
        return 'Invalid Recipients'
    except Exception as e:
        print("ANOTHER EXCEPTION", e)
    smtp_conn.quit()
    print("Message sent!")
    return 'Success'

# REMOVE
@eel.expose
def store_email(folder, uid, subject, from_, to, date, html):
    print(folder, type(uid), type(subject), type(from_), type(to), type(date), type(html))
    # sql_conn = sqlite3.connect('sql.db', timeout=30)
    sql_conn = sqlite3.connect('sql.db')
    cursor = sql_conn.cursor()

    try:
        # table ="""CREATE TABLE {}
        #         (
        #             UID VARCHAR(255), 
        #             SUBJECT VARCHAR(255), 
        #             FROM_ VARCHAR(255), 
        #             TO_ VARCHAR(255), 
        #             DATE VARCHAR(255), 
        #             HTML VARCHAR(255), 
        #         )""".format(folder)
        # cursor.execute(table)
        cursor.execute(f"CREATE TABLE {folder} ( UID VARCHAR(255), SUBJECT VARCHAR(255), FROM_ VARCHAR(255), TO_ VARCHAR(255), DATE VARCHAR(255), HTML VARCHAR(255) )")
    except Exception as e:
        print("ERROR CREATING TABLE")
        print(e)
    

    cursor.execute(f"INSERT INTO {folder} ( UID, SUBJECT, FROM_, TO_, DATE , HTML) VALUES ( ?, ?, ?, ?, ?, ? )", (uid, subject, from_, str(to), date, html) )
    # cursor.execute("""INSERT INTO {} 
    #                (
    #                     UID, SUBJECT, FROM_, TO_, DATE
    #                 ) VALUES ({}, {}, {}, {}, {}, {})
    #                """.format(folder, uid, sub_no_dquote, from_, to, date, html_no_dquote))
    sql_conn.commit()
    cursor.close()

# REMOVE
@eel.expose
def fetch_folder(folder, limit, offset):
    print(folder, limit, offset)
    sql_conn = sqlite3.connect('sql.db')
    cursor = sql_conn.cursor()
    result = cursor.execute(f'SELECT UID, SUBJECT, FROM_, TO_, DATE FROM {folder} LIMIT {limit} OFFSET {offset}')
    # result = cursor.execute(f'SELECT UID, SUBJECT, FROM_, TO_, DATE FROM {folder}')
    fetch = result.fetchall()
    sql_conn.commit()
    cursor.close()
    data = json.dumps(fetch)
    # converting data back to json to add keys
    new_data = json.loads(data)
    new_data[:0] = [['uid','subject','from','to','date']]
    # applying keys to each row of data
    output = [dict(zip(new_data[0], row)) for row in new_data[1:]]
    return output

# REMOVE
@eel.expose
def fetch_email(folder, uid):
    print(folder, uid)
    sql_conn = sqlite3.connect('sql.db')
    cursor = sql_conn.cursor()
    result = cursor.execute(f'SELECT HTML FROM {folder} WHERE UID = {uid}')
    fetch = result.fetchone()
    sql_conn.commit()
    cursor.close()
    return fetch[0].rstrip()

# replaces get emails
def new_get_emails(email_service: str):
    db = SQLiteClient()
    if email_service == 'all':
        print("GETTING ALL")
        emails = db.fetch_all(50, 0)
    else:
        match email_service:
            case 'gmail':
                emails = db.fetch('gmail', 50, 0)
            case 'outlook':
                print("OUTLOOK")
            case 'yahoo':
                emails = db.fetch('yahoo', 50, 0)
    return emails

def start_app():
    """Start Eel with either production or development configuration."""
    # prod for exe
    # eel.init('test')
    # eel.start('index.html', port=8888, geometry={'size': (1280, 800), 'position': (50, 50)})

    # dev
    eel.init('client/src')
    eel_kwargs = dict(
        host='localhost',
        port=8888,
    )
    eel.start({'port': 3000}, geometry={'size': (1280, 800), 'position': (50, 50)}, **eel_kwargs)

if __name__ == '__main__':
    start_app()
    