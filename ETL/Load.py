import sqlite3

conn = sqlite3.connect('news.db')


# Get counter for loop from count in staging DWH
def get_counter_staging():
    count = conn.execute(
        'SELECT COUNT((("Datum"||" "||"Zeit"))) FROM "news_staging" '
        'WHERE ("Datum"||" "||"Zeit") > (SELECT CASE WHEN MAX("Datum_ID"||" "||"Zeit") IS NULL '
        'THEN "2022-01-01 00:00" ELSE MAX("Datum_ID"||" "||"Zeit") END FROM "news_fact") ORDER BY "Datum", "Zeit"')
    conn.commit()
    return count.fetchone()[0]


# Load transformed data into fact table (Core DWH)
def load():
    n = get_counter_staging()
    for i in range(n):
        conn.execute(
            f'INSERT INTO news_fact(Datum_ID, Zeit) '
            f'SELECT Datum, Zeit FROM news_staging '
            f'WHERE "Datum"||" "||"Zeit" > (SELECT CASE WHEN MAX(Datum_ID||" "||Zeit) is null '
            f'THEN "01-01-2022 00:01" ELSE MAX(Datum_ID||" "||Zeit) END FROM news_fact '
            f'ORDER BY Datum_ID, Zeit) ORDER BY Datum, Zeit LIMIT 1 OFFSET 0'
        )
        conn.execute(
            f'INSERT INTO "news_dim"("News_FK") VALUES (last_insert_rowid())'
        )
        conn.execute(
            'UPDATE news_dim SET Titel = X1.Titel FROM '
            '(SELECT T0.ID, T1.Titel FROM news_fact T0 '
            'INNER JOIN news_staging T1 ON T0."Datum_ID" = T1.Datum AND T0.Zeit = T1.Zeit'
            ') X1 WHERE News_FK = X1.ID'
        )
        conn.commit()
    conn.close()
