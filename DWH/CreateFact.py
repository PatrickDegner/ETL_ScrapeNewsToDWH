import sqlite3

conn = sqlite3.connect('news.db')

# create news fact (Core DWH)
def create_news_fact():
    news_fact = (
        'CREATE TABLE IF NOT EXISTS news_fact('
        '"ID" INTEGER PRIMARY KEY AUTOINCREMENT, '
        '"Datum_ID" TEXT, '
        '"Zeit" TEXT)')

    conn.execute(news_fact)
    conn.close()
