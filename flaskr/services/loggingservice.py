from datetime import date, datetime
import flaskr.models.Logging
import sqlite3, os
from flaskr import file_directory

def Logging(LogType,LogDetails):
    LogDateTime = datetime.now()
    conn = sqlite3.connect(os.path.join(file_directory, "storage.db"))
    c = conn.cursor()
    c.execute("INSERT INTO logs (LogDetails,LogType,LogDateTime) VALUES (?, ?, ?)", (LogDetails, LogType, LogDateTime))
    conn.commit()

