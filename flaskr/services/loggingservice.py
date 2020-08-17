from datetime import datetime
import flaskr.models.Logging
import sqlite3, os
from flaskr import file_directory


def Logging(log_type, log_details):
    log_date_time = datetime.now()
    conn = sqlite3.connect(os.path.join(file_directory, "storage.db"))
    c = conn.cursor()
    c.execute("INSERT INTO logs (log_details, log_type, log_date_time) VALUES (?, ?, ?)", (log_details, log_type, log_date_time))
    conn.commit()
