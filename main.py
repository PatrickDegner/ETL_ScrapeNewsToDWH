import logging
import logging.config
import sqlite3

import yaml

from DWH.CreateDims import create_date_dim, create_news_dim
from DWH.CreateFact import create_news_fact
from ETL.Load import load
from ETL.Transform import transform


def main():
    """
        Entry point to run the ETL job
    """
    # Parsing YAML config file
    config_path = 'Configs/etl_report1_config.yml'
    config = yaml.safe_load(open(config_path))
    # Configure logging
    log_config = config['logging']
    logging.config.dictConfig(log_config)
    logger = logging.getLogger(__name__)
    logger.info("Started the ETL run...")

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

    logger.info("Finished the ETL run...")


if __name__ == '__main__':
    main()
