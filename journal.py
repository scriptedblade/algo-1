# -*- coding: utf-8 -*-
"""
Created on Sun Apr  9 10:45:01 2023
# GET TRADE DATA FOR A SPECIFIC DAY
# WORK IN PROGRESS
@author: My Account
"""

from kiteconnect import KiteConnect
import pandas as pd
import datetime
import os

cwd = os.chdir("C:\\Users\\dinnu\\Desktop\\rsi1 python")

#generate trading session
access_token = open("access_token.txt",'r').read()
key_secret = open("api_key.txt",'r').read().split()
kite = KiteConnect(api_key=key_secret[0])
kite.set_access_token(access_token)

trades = kite.trades()
trades_df = pd.DataFrame(trades)

filtered_trades_df = trades_df[['tradingsymbol', 'transaction_type', 'price', 'quantity', 'exchange_timestamp']]
filtered_trades_df.columns = ['instrument_traded', 'transaction_type', 'price', 'quantity', 'exchange_timestamp']

filtered_trades_df['exchange_timestamp'] = pd.to_datetime(filtered_trades_df['exchange_timestamp'])
filtered_trades_df['date'] = filtered_trades_df['exchange_timestamp'].dt.date
filtered_trades_df['day'] = filtered_trades_df['exchange_timestamp'].dt.day_name()

# Define the specific date for which you want to fetch trade data
specific_date = datetime.date(2023, 4, 6)

# Filter the trades for the specific date
specific_day_trades = filtered_trades_df[filtered_trades_df['date'] == specific_date]

print(specific_day_trades)