# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 00:46:24 2023
# TRADE JOURNAL AUTOMATION
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

filtered_trades_df = trades_df[['tradingsymbol', 'transaction_type', 'average_price', 'quantity', 'exchange_timestamp']]
filtered_trades_df.columns = ['instrument_traded', 'transaction_type', 'average_price', 'quantity', 'exchange_timestamp']

filtered_trades_df['exchange_timestamp'] = pd.to_datetime(filtered_trades_df['exchange_timestamp'])
filtered_trades_df['date'] = filtered_trades_df['exchange_timestamp'].dt.date
filtered_trades_df['day'] = filtered_trades_df['exchange_timestamp'].dt.day_name()

buy_trades_df = filtered_trades_df[filtered_trades_df['transaction_type'] == 'BUY']
sell_trades_df = filtered_trades_df[filtered_trades_df['transaction_type'] == 'SELL']

average_buy_price = buy_trades_df['average_price'].mean()
average_sell_price = sell_trades_df['average_price'].mean()

total_buy_quantity = buy_trades_df['quantity'].sum()
total_sell_quantity = sell_trades_df['quantity'].sum()

average_prices_df = pd.DataFrame(
    {'instrument_traded': [buy_trades_df.iloc[0]['instrument_traded']],
     'average_buy_price': [average_buy_price],
     'average_sell_price': [average_sell_price],
     'total_buy_quantity': [total_buy_quantity],
     'total_sell_quantity': [total_sell_quantity],
     'date': [sell_trades_df.iloc[0]['date']],
     'day': [sell_trades_df.iloc[0]['day']]
     })

# Define the Excel file name
excel_file = "trading_journal.xlsx"

# Check if the Excel file exists, if not, create it
if not os.path.isfile(excel_file):
    average_prices_df.to_excel(excel_file, index=False)
else:
    # Read the existing Excel file into a DataFrame
    existing_df = pd.read_excel(excel_file)

    # Append the new data to the existing DataFrame
    updated_df = existing_df.append(average_prices_df, ignore_index=True)

    # Save the updated DataFrame to the same Excel file
    updated_df.to_excel(excel_file, index=False)