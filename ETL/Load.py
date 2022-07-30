import sqlite3

conn = sqlite3.connect('news.db')


# Get counter for loop from count in staging DWH
def get_counter_staging():
    count = conn.execute(
        'SELECT COUNT(*) FROM news_staging '
        'WHERE ((SELECT MAX(Datum||" "||Zeit) FROM news_staging) > '
        '(SELECT CASE WHEN MAX(Datum_ID||" "||Zeit) '
        'IS NULL THEN "2022-01-01 00:00" ELSE MAX(Datum_ID||" "||Zeit) END FROM news_fact))')
    conn.commit()
    return count.fetchone()[0]


# Load transformed data into fact table (Core DWH)
def load():
    counter = 0
    for i in range(get_counter_staging()):
        conn.execute(
            f'INSERT INTO news_fact(Datum_ID, Zeit) '
            f'SELECT Datum, Zeit FROM news_staging '
            f'WHERE ((SELECT MAX(Datum||" "||Zeit) FROM news_staging) > '
            f'(SELECT CASE WHEN MAX(Datum_ID||" "||Zeit)'
            f' IS NULL THEN "2022-01-01 00:00" ELSE MAX(Datum_ID||" "||Zeit) END FROM news_fact)) '
            f'LIMIT 1 OFFSET {counter}'
        )
        conn.execute(
            f'INSERT INTO news_dim(News_FK, Titel) '
            f'SELECT last_insert_rowid(), Titel FROM news_staging LIMIT 1 OFFSET {counter}'

        )
        conn.commit()
        counter += 1
    conn.close()
