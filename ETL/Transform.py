import logging
import re
import sqlite3
from datetime import date

from ETL.Extract import extract

logger = logging.getLogger(__name__)


# Transform output and insert/append into staging DWH
def transform():
    # Setup Database connection
    conn = sqlite3.connect('news.db')
    conn.execute(
        'CREATE TABLE IF NOT EXISTS news_staging ("Datum" TEXT, "Zeit" TEXT, "Titel" TEXT)'
    )
    # Transform to readable output
    for i in extract():
        result = re.split('; |, |\*|\n|\xa0|            ', i.get_text().replace('"', ""))
        conn.execute(
            f'INSERT INTO news_staging("Datum","Zeit","Titel") '
            f'SELECT "{date.today()}","{result[1]}","{result[5]}" '
            f'WHERE NOT EXISTS (SELECT * FROM news_staging WHERE'
            f'"Zeit" = "{result[1]}" AND "Titel" = "{result[5]}")'
        )
    conn.commit()
    conn.close()
