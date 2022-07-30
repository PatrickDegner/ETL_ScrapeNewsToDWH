import sqlite3

from DWH.CreateDims import create_date_dim, create_news_dim
from DWH.CreateFact import create_news_fact
from ETL.Load import load
from ETL.Transform import transform

# Init
conn = sqlite3.connect('news.db')
create_date_dim()
create_news_dim()
create_news_fact()


# ETL
transform()
load()

# Result
result = conn.execute(
    'SELECT date_dim."Datum", '
    'date_dim."Wochentag", '
    'news_fact."Zeit", '
    'news_dim.Titel '
    'FROM news_fact '
    'INNER JOIN date_dim ON news_fact."Datum_ID" = date_dim."Datum"'
    'INNER JOIN news_dim ON news_fact."ID" = news_dim."News_FK"'
    'ORDER BY date_dim."Datum", news_fact."Zeit"')
conn.commit()

for i in (result.fetchall()):
    print(i)

conn.close()
