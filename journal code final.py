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

positions = {}
journal_entries = []

for index, row in filtered_trades_df.iterrows():
    instrument = row['instrument_traded']
    transaction_type = row['transaction_type']
    price = row['average_price']
    quantity = row['quantity']
    date = row['date']
    day = row['day']

    if instrument not in positions:
        positions[instrument] = {"buy_quantity": 0, "buy_value": 0, "sell_quantity": 0, "sell_value": 0}

    if transaction_type == 'BUY':
        positions[instrument]['buy_quantity'] += quantity
        positions[instrument]['buy_value'] += price * quantity
    elif transaction_type == 'SELL':
        positions[instrument]['sell_quantity'] += quantity
        positions[instrument]['sell_value'] += price * quantity

        if positions[instrument]['buy_quantity'] == positions[instrument]['sell_quantity']:
            average_buy_price = positions[instrument]['buy_value'] / positions[instrument]['buy_quantity']
            average_sell_price = positions[instrument]['sell_value'] / positions[instrument]['sell_quantity']

            profit_loss = (average_sell_price - average_buy_price) * positions[instrument]['buy_quantity']
            profit_loss_percentage = (profit_loss / (average_buy_price * positions[instrument]['buy_quantity'])) * 100

            journal_entries.append({
                "Date": date,
                "Day": day,
                "Instrument": instrument,
                "Average Buy": average_buy_price,
                "Average Sell": average_sell_price,
                "Quantity": positions[instrument]['buy_quantity'],
                "P/L": profit_loss,
                "P/L%": profit_loss_percentage,
                
            })

            positions[instrument] = {"buy_quantity": 0, "buy_value": 0, "sell_quantity": 0, "sell_value": 0}

journal_df = pd.DataFrame(journal_entries)

excel_file = "trading_journal.xlsx"

if not os.path.isfile(excel_file):
    journal_df.to_excel(excel_file, index=False)
else:
    existing_df = pd.read_excel(excel_file)
    updated_df = pd.concat([existing_df, journal_df], ignore_index=True)
    updated_df.to_excel(excel_file, index=False)