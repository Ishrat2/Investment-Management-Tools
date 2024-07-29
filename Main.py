#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 15:13:51 2023

@author: ishratvasid
"""

import numpy as np
import pandas as pd
import sys
sys.path.append("/Users/ishratvasid/Desktop/GitHub/Investment-Management-Tools/Portfolio-Construction")

import portfolio_risk_tool as prt
from getYahooPriceReturn import getYahooPriceReturn 

start_date = '2004-05-31'
end_date =  '2024-06-30'
tickers = ['ASIANPAINT', 'AXISBANK', 'BAJAJFINSV', 'BHARATFORG', 'CDSL', 'COROMANDEL', 'CRISIL', 'DELTACORP', 'DIVISLAB', 'DMART', 'GODREJIND', 'HDFCAMC', 'ITC', 'JUBLFOOD', 'KOTAKBANK', 'KPRMILL',
           'LT', 'M&M', 'MCDOWELL-N', 'NRBBEARING', 'NUCLEUS', 'SBILIFE', 'SBIN', 'SJVN', 'TATACOMM', 'TATAELXSI', 
           'TATAMOTORS', 'TITAN', 'UBL', 'ULTRACEMCO', 'AFFLE', 'DEVYANI', 'IRCTC', 'MAPMYINDIA', 'SBICARD']
tickers = [ticker + '.NS' for ticker in tickers]
   
daily_return = getYahooPriceReturn(tickers, start_date, end_date)
daily_return = daily_return[1:].dropna(axis=1)
daily_return.index = pd.to_datetime(daily_return.index, format="%YYYY-%m-%d %HH:%MM:%SS")
daily_return.index = daily_return.index.to_period('M')

def daily_to_monthly(daily_return):
    monthly_return = (daily_return + 1).prod()-1
    return monthly_return
monthly_return = {}
for i in daily_return.columns:    
    ticker_monthly_return = daily_return.groupby(['Date'],axis=0).agg({i:daily_to_monthly})
    monthly_return[i] = ticker_monthly_return

monthly_data = pd.concat(monthly_return, axis=1)    
monthly_data.columns = monthly_data.columns.get_level_values(0)

# 1. Performance Matrices
ann_ret = prt.annualize_rets(monthly_data, 12).sort_values()
ann_vol = prt.annualize_vol(monthly_data, 12).sort_values()
sharpe = prt.sharpe_ratio(monthly_data, 0.03, 12).sort_values()
#mdd = prt.drawdown(monthly_data)
cov = monthly_data.cov()

# 2. Plot Efficient Frontier
n_points = len(monthly_data.columns)
weights = np.repeat(1/n_points, n_points)
port_ret = prt.portfolio_return(weights, ann_ret)
port_vol = prt.portfolio_vol(weights, cov)

ax = prt.plot_ef(25, ann_ret, cov)
ax.set_xlim(left=0)

# 3. Fund Seperation Theorem and Capital Market Line
# get MSR
rf = 0.2
w_msr = prt.msr(rf, ann_ret, cov)
r_msr = prt.portfolio_return(w_msr, ann_ret)
vol_msr = prt.portfolio_vol(w_msr, cov)
# add CML
cml_x = [0, vol_msr]
cml_y = [rf, r_msr]
ax.plot(cml_x, cml_y, color='green', marker='o', linestyle='dashed', linewidth=2, markersize=12)
#Plot EF with CML 
prt.plot_ef(20, ann_ret, cov, style='-', show_cml=True, riskfree_rate=0.2)