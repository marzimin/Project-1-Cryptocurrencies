# data_loading_phase3
# shift option f to use autopep8 in VS Code

# Import packages, data in csvs - check filepaths
import psycopg2
from sqlalchemy import create_engine
import pandas as pd
import pandas_ta as ta
from ta import add_all_ta_features  # This auto calculates your TI columns
from ta.utils import dropna

# Script to get it ready for EDA


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

# load data from your postgres database instead:


# DSN (data source name) format for database connections:
# [protocol / database  name]://[username]:[password]@[hostname / ip]:[port]/[database name here]

# on your computer you are the user postgres (full administrative access)
# Will be different (provided) for remote servers
db_user = 'postgres'

# if you need a password to access a database, put it here
# Passwords will be required if you're accessing a remote server
db_password = ''

# on your computer, use localhost
# will be different for remote servers
db_host = 'localhost'

# the default port for postgres is 5432
db_port = 5432

# we want to connect to a standard database
# check your postgres app for available local databases
database = 'marzimin'

# Code syntax to read the database:

conn_str = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}'

# Create engine
engine = create_engine(conn_str+f'/{database}')

query = f"""
      SELECT tablename
      FROM pg_catalog.pg_tables
      WHERE schemaname != 'pg_catalog' AND 
      schemaname != 'information_schema'
         ;"""

print("Available data: ", pd.read_sql(query, engine))

# Queries for base:
# Checking with psql shows public to be schema for all tables in this database

btcq = f""" SELECT * FROM "BTCUSD"; """
ethq = f""" SELECT * FROM "ETHUSD"; """
ltcq = f""" SELECT * FROM "LTCUSD"; """
xlmq = f""" SELECT * FROM "XLMUSD"; """
dashq = f""" SELECT * FROM "DASHUSD"; """
linkq = f""" SELECT * FROM "LINKUSD"; """

# Queries for TA csvs:
btctaq = f""" SELECT * FROM "BTC_TA"; """
ethtaq = f""" SELECT * FROM "ETH_TA"; """
ltctaq = f""" SELECT * FROM "LTC_TA"; """
xlmtaq = f""" SELECT * FROM "XLM_TA"; """
dashtaq = f""" SELECT * FROM "DASH_TA"; """
linktaq = f""" SELECT * FROM "LINK_TA"; """

# Base OHLCV data
btc = pd.read_sql(btcq, engine)
btc_cln = df_time_cln(btc)

eth = pd.read_sql(ethq, engine)
eth_cln = df_time_cln(eth)

ltc = pd.read_sql(ltcq, engine)
ltc_cln = df_time_cln(ltc)

xlm = pd.read_sql(xlmq, engine)
xlm_cln = df_time_cln(xlm)

dash = pd.read_sql(dashq, engine)
dash_cln = df_time_cln(dash)

link = pd.read_sql(linkq, engine)
link_cln = df_time_cln(link)

# Data with TIs
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

# Function to resample to daily plots


def time_ohlcv_converter(df, time, o='open', h='high', l='low', c='close', v='volume'):
    """ Takes a financial time series dateindexed dataframe (OHLCV)
        and resamples/aggregates them to a new date index. """

    # copy so it won't overwrite
    df1 = df.copy()

    # 'D' for daily, .first() for first value in open
    df1['open_{}'.format(time)] = df1[o].resample(time).first()

    # .max() for highest value in range
    df1['high_{}'.format(time)] = df1[h].resample(time).max()

    # .min() for lowest value in range
    df1['low_{}'.format(time)] = df1[l].resample(time).min()

    # .last() for most recent value in close
    df1['close_{}'.format(time)] = df1[c].resample(time).last()

    # .sum() for aggregated volume daily
    df1['volume_{}'.format(time)] = df1[v].resample(time).sum()

    # drop hourly data
    df1.dropna(how='any', inplace=True)
    df1.drop(columns=['open', 'high', 'low', 'close', 'volume'], inplace=True)

    return df1


# Your daily resampled dfs
btc_d = time_ohlcv_converter(btc_cln, 'D')
eth_d = time_ohlcv_converter(eth_cln, 'D')
ltc_d = time_ohlcv_converter(ltc_cln, 'D')
xlm_d = time_ohlcv_converter(xlm_cln, 'D')
dash_d = time_ohlcv_converter(dash_cln, 'D')
link_d = time_ohlcv_converter(link_cln, 'D')

# Daily resampled dfs with TA library function
btc_dta = add_all_ta_features(
    btc_d, open="open_D", high="high_D", low="low_D",
    close="close_D", volume="volume_D", fillna=True)

eth_dta = add_all_ta_features(
    eth_d, open="open_D", high="high_D", low="low_D",
    close="close_D", volume="volume_D", fillna=True)

ltc_dta = add_all_ta_features(
    ltc_d, open="open_D", high="high_D", low="low_D",
    close="close_D", volume="volume_D", fillna=True)

xlm_dta = add_all_ta_features(
    xlm_d, open="open_D", high="high_D", low="low_D",
    close="close_D", volume="volume_D", fillna=True)

dash_dta = add_all_ta_features(
    dash_d, open="open_D", high="high_D", low="low_D",
    close="close_D", volume="volume_D", fillna=True)

link_dta = add_all_ta_features(
    link_d, open="open_D", high="high_D", low="low_D",
    close="close_D", volume="volume_D", fillna=True)

print("All done. For now just add for example data_loading_phase_3.btc_dta as a variable for your data.")
