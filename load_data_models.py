# Test script to load crypto datasets - phase 4 models only
# phase3 script more descriptive
# shift option f to use autopep8 in VS Code (.py files only)

# Package imports
import pandas as pd
import psycopg2
from sqlalchemy import create_engine


def df_time_cln(df):
    """ Quickly cleans your time series df, converting index to a datetime
        format and sorting it chronologically. Loading from csv will create a
        new index column so you have to run this everytime after importing. """

    df1 = df.copy()

    df1.index = df1['time']
    df1.drop(columns='time', inplace=True)
    df1.sort_index(inplace=True)  # Sort chronologically
    df1.index = pd.to_datetime(df1.index)

    return df1


# Local postgres database only
db_user = 'postgres'
db_password = ''
db_host = 'localhost'
db_port = 5432
database = 'marzimin'

conn_str = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}'
engine = create_engine(conn_str+f'/{database}')

query = f"""
      SELECT tablename
      FROM pg_catalog.pg_tables
      WHERE schemaname != 'pg_catalog' AND 
      schemaname != 'information_schema'
         ;"""

print("Available data: ", pd.read_sql(query, engine))


# Queries for TA csvs:
btctaq = f""" SELECT * FROM "BTC_TA"; """
ethtaq = f""" SELECT * FROM "ETH_TA"; """
ltctaq = f""" SELECT * FROM "LTC_TA"; """
xlmtaq = f""" SELECT * FROM "XLM_TA"; """
dashtaq = f""" SELECT * FROM "DASH_TA"; """
linktaq = f""" SELECT * FROM "LINK_TA"; """


# Load data
btc_ta = pd.read_sql(btctaq, engine)
btc_ta = df_time_cln(btc_ta)

eth_ta = pd.read_sql(ethtaq, engine)
eth_ta = df_time_cln(eth_ta)

ltc_ta = pd.read_sql(ltctaq, engine)
ltc_ta = df_time_cln(ltc_ta)

xlm_ta = pd.read_sql(xlmtaq, engine)
xlm_ta = df_time_cln(xlm_ta)

dash_ta = pd.read_sql(dashtaq, engine)
dash_ta = df_time_cln(dash_ta)

link_ta = pd.read_sql(linktaq, engine)
link_ta = df_time_cln(link_ta)

print("Data Loaded. For now just add for example btc_ta = data_loading_phase_4.btc_ta as a variable for your data.")
