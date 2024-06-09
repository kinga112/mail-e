import json
import sqlite3
import re

SQL_DATABASE = 'test_sql.db'

class SQLiteClient:
    """
    SQLite Client interacts with database built
    to fetch and store emails in db as cache
    """
    def __init__(self):
        conn = sqlite3.connect(SQL_DATABASE)
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
        table ='''CREATE TABLE AllEmails 
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
                    )'''
        try:
            cursor.execute(table)
        except Exception as e:
            # print(e)
            pass

        table = '''CREATE TABLE Folders
                    ( 
                        FOLDER VARCHAR(255) PRIMARY KEY UNIQUE
                    )'''
        try:
            cursor.execute(table)
        except Exception as e:
            # print(e)
            pass
        
    def fetch(self, email_service: str, limit: int, offset: int):
        """
        Fetch emails from specific email service provider using limit and offset bounds.
        :return: list of emails in json format
        """
        conn = sqlite3.connect(SQL_DATABASE)
        cursor = conn.cursor()
        result = cursor.execute(f'''SELECT SERVICE, SEEN, FLAGGED, UID, SUBJECT, FROM_, TO_, DATE 
                                    FROM AllEmails WHERE SERVICE = "{email_service}" 
                                    ORDER BY datetime(DATE) DESC LIMIT {limit} OFFSET {offset}''')
        fetch = result.fetchall()
        cursor.close()
        conn.close()
        # convert fetch data into json format
        json_data = json.dumps(fetch)
        # converting data back to python obj in json format
        data = json.loads(json_data)
        data[:0] = [['service', 'seen', 'flagged', 'uid', 'subject', 'from', 'to', 'date']]
        # applying keys to each row of data
        output = [dict(zip(data[0], row)) for row in data[1:]]
        return output
        
    def fetch_all(self, limit: int, offset: int):
        """
        Fetch emails from all accounts using limit and offset bounds.
        :return: list of emails in json format
        """
        conn = sqlite3.connect(SQL_DATABASE)
        cursor = conn.cursor()
        result = cursor.execute(f'''SELECT SERVICE, SEEN, FLAGGED, UID, SUBJECT, FROM_, TO_, DATE 
                                    FROM AllEmails ORDER BY datetime(DATE) DESC LIMIT {limit} OFFSET {offset}''')
        fetch = result.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        # convert fetch data into json format
        json_data = json.dumps(fetch)
        # converting data back to python obj in json format
        data = json.loads(json_data)
        data[:0] = [['service', 'seen', 'flagged', 'uid', 'subject', 'from', 'to', 'date']]
        # applying keys to each row of data
        output = [dict(zip(data[0], row)) for row in data[1:]]
        return output
        
    def fetch_email(self, email_service: str, uid: str):
        """
        Fetch email message in html format.
        :return: html string
        """
        conn = sqlite3.connect(SQL_DATABASE)
        cursor = conn.cursor()
        result = cursor.execute(f'SELECT HTML FROM AllEmails WHERE UID = "{uid}" AND SERVICE = "{email_service}"')
        fetch = result.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return fetch[0].rstrip()

    def add_to_folder(self, folder: list, key: str):
        # print(f"folder: {folder[0]}, uid: {key}")
        sql_query = """SELECT name FROM sqlite_master WHERE type='table';"""
        conn = sqlite3.connect(SQL_DATABASE)
        cursor = conn.cursor()
        cursor.execute(sql_query)
        try:
            cursor.execute(f'''INSERT INTO "{folder[0]}" 
                            ( UNIQUEKEY ) 
                            VALUES ( ? )''', 
                            (key, ))
            conn.commit()
            return
        except Exception as e:
            print("Exception:", e)
            return 'Email Exists'
        finally:
            cursor.close()
            conn.close()
        
    def create_folder(self, folder: str):
        conn = sqlite3.connect(SQL_DATABASE)
        cursor = conn.cursor()
        print("Creating Folder:", folder)
        table =f'''CREATE TABLE "{folder}" 
                    ( 
                        UNIQUEKEY VARCHAR(255) PRIMARY KEY UNIQUE
                    )'''
        try:
            cursor.execute(table)
        except Exception as e:
            print("Exception:", e)
            pass
        try:
            cursor.execute('''INSERT INTO Folders 
                           ( FOLDER ) 
                           VALUES ( ? )''', 
                           (folder, ))
            conn.commit()
            return 'Success'
        except Exception as e:
            print("Exception:", e)
            return 'Duplicate'
        finally:
            cursor.close()
            conn.close()
    
    def fetch_folder(self, folder: str):
        conn = sqlite3.connect(SQL_DATABASE)
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM "{folder[0]}"')
        folder_emails = cursor.fetchall()
        output = []
        for result in folder_emails:
            key: str = result[0]
            if 'gmail' in key:
                uid = key.split('gmail')[0]
                service = 'gmail'
            if 'outlook' in key:
                uid = key.split('outlook')[0]
                service = 'outlook'
            
            result = cursor.execute(f'''SELECT SERVICE, SEEN, FLAGGED, UID, SUBJECT, FROM_, TO_, DATE 
                                    FROM AllEmails WHERE UID = "{uid}" AND SERVICE = "{service}" ORDER BY datetime(DATE)''')
            fetch = result.fetchall()
            # convert fetch data into json format
            json_data = json.dumps(fetch)
            # converting data back to python obj in json format
            data = json.loads(json_data)
            data[:0] = [['service', 'seen', 'flagged', 'uid', 'subject', 'from', 'to', 'date']]
            # applying keys to each row of data
            output.append([dict(zip(data[0], row)) for row in data[1:]][0])
        return output

    
    def list_folders(self):
        """
        List all from Folders table
        :return: list of strings
        """
        conn = sqlite3.connect(SQL_DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Folders')
        tables = cursor.fetchall()
        return tables
    
    def store_email(self, uniquekey: str, email_service: str, seen: str, flagged: str, uid: str, subject: str, from_: str, to: str, date: str, html: str):
        """
        Store email in DB for quick fetch.
        :return: 'Done' on duplicate to stop loop, None to continue fetching.
        """
        conn = sqlite3.connect(SQL_DATABASE)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''INSERT INTO AllEmails 
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
