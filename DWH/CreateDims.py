import sqlite3

conn = sqlite3.connect('news.db')


# Setup date dimension
def create_date_dim():
    date_dim = ('''
    CREATE TABLE IF NOT EXISTS date_dim AS
    WITH RECURSIVE
    
    rDateDimensionMinute (CalendarDateInterval)
    AS
        (
            SELECT datetime('2022-01-01 00:00:00')
            UNION ALL
            SELECT datetime(CalendarDateInterval, '+24 hour') FROM rDateDimensionMinute
            LIMIT 100000
        )
    SELECT
        date(CalendarDateInterval) as "Datum",
        strftime('%w',CalendarDateInterval)	"Tag",
        case cast (strftime('%w', CalendarDateInterval) as integer)
        when 0 then 'Sonntag'
        when 1 then 'Montag'
        when 2 then 'Dienstag'
        when 3 then 'Mittwoch'
        when 4 then 'Donnerstag'
        when 5 then 'Freitag'
        when 6 then 'Samstag' end "Wochentag",
        substr('SoMoDiMiDoFrSa', 1 + 2*strftime('%w', CalendarDateInterval), 2) "WochentagKurz",
        strftime('%d',CalendarDateInterval)	"TagImMonat",
        case cast (strftime('%w', CalendarDateInterval) as integer)
        when 0 then 1
        when 6 then 1
        else 0 end "IstWochenende",
        case cast (strftime('%w', CalendarDateInterval) as integer)
        when 0 then 0
        when 6 then 0
        else 1 end "IstWochentag",
        strftime('%m',CalendarDateInterval)	"Monat",
        case strftime('%m', date(CalendarDateInterval))
            when '01' then 'Januar'
            when '02' then 'Februar'
            when '03' then 'März'
            when '04' then 'April'
            when '05' then 'Mai'
            when '06' then 'Juni'
            when '07' then 'Juli'
            when '08' then 'August'
            when '09' then 'September'
            when '10' then 'Oktober'
            when '11' then 'November'
            when '12' then 'Dezember' else '' end "MonatName",
        case strftime('%m', date(CalendarDateInterval))
            when '01' then 'Jan'
            when '02' then 'Feb'
            when '03' then 'Mär'
            when '04' then 'Apr'
            when '05' then 'Mai'
            when '06' then 'Jun'
            when '07' then 'Jul'
            when '08' then 'Aug'
            when '09' then 'Sep'
            when '10' then 'Okt'
            when '11' then 'Nov'
            when '12' then 'Dez' else '' end "MonatKurz",
        strftime('%Y',CalendarDateInterval)	"JahrZahl"
    FROM rDateDimensionMinute;
    ''')
    conn.execute(date_dim)


# setup news dimension
def create_news_dim():
    news_dim = (
        'CREATE TABLE IF NOT EXISTS news_dim ('
        '"ID" INTEGER PRIMARY KEY AUTOINCREMENT, '
        '"News_FK" INTEGER, '
        '"Titel" TEXT, '
        'FOREIGN KEY("News_FK") REFERENCES news_fact("ID"))')

    conn.execute(news_dim)
    conn.close()



