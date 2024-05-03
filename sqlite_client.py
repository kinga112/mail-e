import json
import sqlite3

class SQLiteClient:
    """
    SQLite Client interacts with database built
    to fetch and store emails in db as cache
    """
    def __init__(self):
        conn = sqlite3.connect('new_sql.db')
        cursor = conn.cursor()
        # UNIQUEKEY: *Primary Key* '{user}{uid}' combines user and uid
        # SERVICE: service provider: 'gmail', 'yahoo'
        # SEEN: if the email has been seen or not: 'True'/'False'
        # FLAGGED: if emails is starred: 'True'/'False'
        # UID: unique email id from imap server
        # SUBJECT: subject of email
        # FROM_: from address
        # TO_: to address
        # DATE: date string of when email was sent/received
        # HTML: html string of email
        table ="""CREATE TABLE AllEmails 
                    ( 
                        UNIQUEKEY VARCHAR(255) PRIMARY KEY UNIQUE,
                        SERVICE VARCHAR(255), 
                        SEEN VARCHAR(255), 
                        FLAGGED VARCHAR(255), 
                        UID VARCHAR(255), 
                        SUBJECT VARCHAR(255), 
                        FROM_ VARCHAR(255), 
                        TO_ VARCHAR(255), 
                        DATE VARCHAR(255), 
                        HTML VARCHAR(255) 
                    )"""
        try:
            cursor.execute(table)
        except Exception as e:
            print(e)
        
    def fetch(self, email_service: str, limit: int, offset: int):
        """
        Fetch emails from specific email service provider using limit and offset bounds.
        :return: list of emails in json format
        """
        conn = sqlite3.connect('new_sql.db')
        cursor = conn.cursor()
        result = cursor.execute(f'''SELECT SEEN, FLAGGED, UID, SUBJECT, FROM_, TO_, DATE 
                                FROM AllEmails LIMIT {limit} OFFSET {offset} 
                                WHERE SERVICE = {email_service}''')
        fetch = result.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        data = json.dumps(fetch)
        # converting data back to json to add keys
        new_data = json.loads(data)
        new_data[:0] = [['seen', 'flagged', 'uid', 'subject', 'from', 'to', 'date']]
        # applying keys to each row of data
        output = [dict(zip(new_data[0], row)) for row in new_data[1:]]
        return output
        
    def fetch_all(self, limit: int, offset: int):
        """
        Fetch emails from all accounts using limit and offset bounds.
        :return: list of emails in json format
        """
        conn = sqlite3.connect('new_sql.db')
        cursor = conn.cursor()
        result = cursor.execute(f'SELECT SERVICE, SEEN, FLAGGED, UID, SUBJECT, FROM_, TO_, DATE FROM AllEmails LIMIT {limit} OFFSET {offset}')
        fetch = result.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        data = json.dumps(fetch)
        # converting data back to json to add keys
        new_data = json.loads(data)
        new_data[:0] = [['service', 'seen', 'flagged', 'uid','subject','from','to','date']]
        # applying keys to each row of data
        output = [dict(zip(new_data[0], row)) for row in new_data[1:]]
        return output
        
    def fetch_email(self, email_service: str, uid: str):
        """
        Fetch email message in html format.
        :return: html string
        """
        conn = sqlite3.connect('new_sql.db')
        cursor = conn.cursor()
        result = cursor.execute(f'SELECT HTML FROM AllEmails WHERE UID = {uid} AND SERVICE = {email_service}')
        fetch = result.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return fetch[0].rstrip()
    
    # think about how to create unique all emails, but if user logs out then it would still be connected to this db
    def store_email(self, uniquekey: str, email_service: str, seen: str, flagged: str, uid: str, subject: str, from_: str, to: str, date: str, html: str):
        """
        Store email in DB for quick fetch.
        :return: 'Done' on successful add, None if duplicate.
        """
        conn = sqlite3.connect('new_sql.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute(f'''INSERT INTO AllEmails 
                           ( UNIQUEKEY, SERVICE, SEEN, FLAGGED, UID, SUBJECT, FROM_, TO_, DATE , HTML ) 
                           VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )''', 
                           (uniquekey, email_service, seen, flagged, uid, subject, from_, to, date, html))
            conn.commit()
            return
        except:
            return 'Done'
        finally:
            cursor.close()
            conn.close()
