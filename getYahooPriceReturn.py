#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 13:14:53 2024

@author: ishratvasid
"""

import pandas as pd
import yfinance as yf

def getYahooPriceReturn(tickers_list, start_date, end_date):
    stock_data = {}
    # Loop through each ticker and download the data
    for ticker in tickers_list:
        data = yf.download(ticker, start=start_date, end=end_date)['Adj Close']
        stock_data[ticker] = data
    
    # Convert the dictionary to a Pandas DataFrame
    combined_data = pd.concat(stock_data, axis=1)
    combined_data = combined_data.sort_index()
   
    # Get the data for this tickers from yahoo finance
    total_return = combined_data.pct_change()
    return total_return