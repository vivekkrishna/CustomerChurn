# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 20:38:38 2017

@author: choppak
"""
import pandas as pd
def getfeatures(date):
    
    df = pd.read_csv("customer_status_history_train.csv",sep='\t')
    #status = df.filter(df.snapshot_day <= prediction_dt).toPandas()
    statusA = df[df['snapshot_day']<=endDate]
    statusA.snapshot_day = pd.to_datetime(statusA.snapshot_day, format='%Y-%m-%d')
    prior_month = statusA.groupby('customer_id')
    
    xr = prior_month.last()
#     xr[xr.ku_status == 'PAID ACTIVE'].index
    xr['ku_status'] = xr['ku_status'].map({'PAID ACTIVE': 1, 'PAID CANCELLED': 0})
    
    
    
#     print prior_month.head(20).to_string()
    res = prior_month['snapshot_day'].agg({'enter': 'first', 'exit': 'last'})

    res['time_diff'] = res['exit'] - res['enter']

    res.time_diff = res.time_diff.dt.days
    
    res.drop(['enter','exit'], axis=1, inplace=True)
             
    timeAndLast = pd.merge(res,xr, right_index=True, left_index=True, how="left")
    
    timeAndLast.drop(['snapshot_day'], axis=1, inplace=True)
    
    timeAndLast.rename(columns={'ku_status': 'last_status'}, inplace=True)

    return timeAndLast

features = getfeatures('2017-08-31')

print features.head(5).tostring()