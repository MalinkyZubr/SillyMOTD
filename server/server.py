import os
import sqlite3
import typing

from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime


class MessageTemplate(BaseModel):
    message_title: str
    message: str
    emotion: str
    time_date_sent: datetime


class DatabaseManager:
    INTANTIATE_DATABASE_MESSAGES = """CREATE TABLE MessageHistory(
MessageID INTEGER PRIMARY KEY,
MessageTitle VARCHAR(255),
MessageContent VARCHAR(32768),
DateTime DATETIME DEFAULT CURRENT_TIMESTAMP
);   
"""
    INSTANTIATE_DATABASE_USERS = """CREATE TABLE Users(
    UserID INTEGER PRIMARY KEY,
    UserName VARCHAR(255) UNIQUE,
    MostRecentMessageId INT
);"""

    GET_USER = "SELECT * FROM Users WHERE UserName = ?;"

    database_connection: sqlite3.Connection | None = None

    def __init__(self, sqlite_filepath: str):
        self.database_filename = sqlite_filepath
        self.initialize_db(sqlite_filepath)

    def run_sqlite_opt(self, operation: str, parameters: tuple[any] = tuple()) -> list[any] | None:
        result: list[any] = None
        if(self.database_connection):
            cursor: sqlite3.Cursor = self.database_connection.cursor()
            result = cursor.execute(operation, parameters).fetchall()
            self.database_connection.commit()
            cursor.close()

        return result

    def initialize_db(self, database_filename):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        directory_content = os.listdir(dir_path)
        db_path = f"{dir_path}/{database_filename}"

        if self.database_filename in directory_content:
            self.database_connection = sqlite3.connect(db_path)
        else:
            with open(db_path, "w") as f:
                pass
            self.database_connection = sqlite3.connect(db_path)
            self.run_sqlite_opt(self.INTANTIATE_DATABASE_MESSAGES)
            self.run_sqlite_opt(self.INSTANTIATE_DATABASE_USERS)

    def create_user(self, username: str) -> bool:
        try:
            self.run_sqlite_opt(f"INSERT INTO Users (UserName, MostRecentMessageId) VALUES (?, ?);", (username, 0))
            return True
        except sqlite3.IntegrityError:
            return False
        
    def push_message_to_db(self, message: MessageTemplate):
        pass
        
    def poll_messages(self, user_name: str):
        user: tuple = self.run_sqlite_opt(self.GET_USER, (user_name,))[0]
        print(user)
        uid, name, mid = user
        result = self.run_sqlite_opt(f"SELECT * FROM MessageHistory WHERE MessageID > ?;", (mid,)) 
        print(result)
        return result
    
    def cleanup(self):
        self.database_connection.commit()
        self.database_connection.close()


# class CustomApp(FastAPI):
#     id_counter: int
#     sql_connection: any

#     def configure_custom_features(config_filepath):
#         pass



# @app.post("/message")
# async def push_message(message: MessageTemplate):

if __name__ == "__main__":
    db_conn = DatabaseManager(r"db.db")
    db_conn.create_user("TestZXoober")
    db_conn.poll_messages("TestZXoober")
    db_conn.cleanup()