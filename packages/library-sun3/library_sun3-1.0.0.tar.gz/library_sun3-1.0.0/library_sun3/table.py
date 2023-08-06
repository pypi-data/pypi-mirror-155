# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 20:05:53 2022

@author: Guanhui Sun
"""

from library_sun3.store_lib import*
import datetime
import time
from sqlalchemy import create_engine
from sqlalchemy import text
import pandas as pd
from math import isnan

# Function slightly modified from polygon sample code to format the date string
def ts_to_datetime(ts) -> str:
    return datetime.datetime.fromtimestamp(ts / 1000.0).strftime('%Y-%m-%d %H:%M:%S')

# Function which clears the raw data tables once we have aggregated the data in a 6 minute interval
def reset_raw_data_tables(engine, currency_pairs):
    with engine.begin() as conn:        
        conn.execute(text("DROP TABLE "+currency_pairs[0]+currency_pairs[1]+"_raw;"))
        conn.execute(text("CREATE TABLE "+currency_pairs[0]+currency_pairs[1]+"_raw(ticktime text, fxrate  numeric, inserttime text);"))

# This creates a table for storing the raw, unaggregated price data for each currency pair in the SQLite database
def initialize_raw_data_tables(engine, currency_pairs):
    with engine.begin() as conn:
        conn.execute(text("CREATE TABLE "+currency_pairs[0]+currency_pairs[1]+"_raw(ticktime text, fxrate  numeric, inserttime text);"))

# This creates a table for storing the (6 min interval) aggregated price data for each currency pair in the SQLite database
def initialize_aggregated_tables(engine, currency_pairs):
    with engine.begin() as conn:
        conn.execute(text("CREATE TABLE "+currency_pairs[0]+currency_pairs[1]+"_agg(inserttime text, maxfxrate numeric, minfxrate numeric, volfxrate numeric, avgfxrate  numeric);"))

# This creates a table for storing the (6 min interval) aggregated price data for each currency pair in the SQLite database after 20 periods 
def initialize_aggregated_table_1(engine,currency_pairs):
    with engine.begin() as conn:
        conn.execute(text("CREATE TABLE "+currency_pairs[0]+currency_pairs[1]+"_agg1(inserttime text, maxfxrate numeric, minfxrate numeric, volfxrate numeric, avgfxrate  numeric, FD numeric);"))
    
    

# This function is called every 6 minutes to aggregate the data, store it in the aggregate table,
# and then delete the raw data
def aggregate_raw_data_tables(engine,currency_pairs):
    with engine.begin() as conn:
        result = conn.execute(text("SELECT AVG(fxrate) as avg_price, COUNT(fxrate) as tot_count FROM "+currency_pairs[0]+currency_pairs[1]+"_raw;"))
        for row in result:
            avg_price = row.avg_price
            tot_count = row.tot_count
        max_res = conn.execute(text("SELECT MAX(fxrate) as max_price FROM "+currency_pairs[0]+currency_pairs[1]+"_raw;"))
        for row in max_res:
            max_price = row.max_price
        min_res = conn.execute(text("SELECT MIN(fxrate) as min_price FROM "+currency_pairs[0]+currency_pairs[1]+"_raw;"))
        for row in min_res:
            min_price = row.min_price
        vol_res = conn.execute(text("SELECT "+str(max_price)+" - "+str(min_price)+" as vol_price FROM "+currency_pairs[0]+currency_pairs[1]+"_raw;"))
        for row in vol_res:
            vol_price = row.vol_price
        date_res = conn.execute(text("SELECT MAX(ticktime) as last_date FROM "+currency_pairs[0]+currency_pairs[1]+"_raw;"))
        for row in date_res:
            last_date = row.last_date
        conn.execute(text("INSERT INTO "+currency_pairs[0]+currency_pairs[1]+"_agg (inserttime, maxfxrate, minfxrate, volfxrate, avgfxrate) VALUES (:inserttime, :maxfxrate, :minfxrate, :volfxrate, :avgfxrate);"),[{"inserttime": last_date, "minfxrate": min_price, "maxfxrate": max_price, "volfxrate": vol_price,"avgfxrate": avg_price}])
            
        # This calculates and stores the return values
        exec("currency_pairs[2].append(currency_pair_return(last_date,avg_price,vol_price))")
            
            
        if len(currency_pairs[2]) > 5:
            try:
                avg_pop_value = currency_pairs[2][-6].hist_return
            except:
                avg_pop_value = 0
            if isnan(avg_pop_value) == True:
                avg_pop_value = 0
        else:
            avg_pop_value = 0
        # Calculate the average return value and print it/store it
        curr_avg = currency_pairs[2][-1].get_avg(avg_pop_value)
        
            
        # Now that we have the average return, loop through the last 5 rows in the list to start compiling the 
        # data needed to calculate the standard deviation
        for row in currency_pairs[2][-5:]:
            row.add_to_running_squared_sum(curr_avg)
            
        # Calculate the standard dev using the avg
        curr_std = currency_pairs[2][-1].get_std()
        
        # Calculate the average standard dev
        if len(currency_pairs[2]) > 5:
            try:
                pop_value = currency_pairs[2][-6].std_return
            except:
                pop_value = 0
        else:
            pop_value = 0
        curr_avg_std = currency_pairs[2][-1].get_avg_std(pop_value)
                   
            
def aggregate_raw_data_table_1(engine,currency_pairs):
    with engine.begin() as conn:
        FD_count = 0
        result = conn.execute(text("SELECT AVG(fxrate) as avg_price, COUNT(fxrate) as tot_count FROM "+currency_pairs[0]+currency_pairs[1]+"_raw;"))
        for row in result:
            avg_price = row.avg_price
            tot_count = row.tot_count 
        max_res = conn.execute(text("SELECT MAX(fxrate) as max_price FROM "+currency_pairs[0]+currency_pairs[1]+"_raw;"))
        for row in max_res:
            max_price = row.max_price
        min_res = conn.execute(text("SELECT MIN(fxrate) as min_price FROM "+currency_pairs[0]+currency_pairs[1]+"_raw;"))
        for row in min_res:
            min_price = row.min_price
        vol_res = conn.execute(text("SELECT MAX(fxrate) - MIN(fxrate) as vol_price FROM "+currency_pairs[0]+currency_pairs[1]+"_raw;"))
        for row in vol_res:
            vol_price = row.vol_price
        date_res = conn.execute(text("SELECT MAX(ticktime) as last_date FROM "+currency_pairs[0]+currency_pairs[1]+"_raw;"))
        for row in date_res:
            last_date = row.last_date
        
        # This calculates and stores the return values
        exec("currency_pairs[2].append(currency_pair_return(last_date,avg_price,vol_price))")
            
        if len(currency_pairs[2]) > 5:
            try:
                avg_pop_value = currency_pairs[2][-6].hist_return
            except:
                avg_pop_value = 0
            if isnan(avg_pop_value) == True:
                avg_pop_value = 0
        else:
            avg_pop_value = 0
        # Calculate the average return value and print it/store it
        curr_avg = currency_pairs[2][-1].get_avg(avg_pop_value)
            
        # Now that we have the average return, loop through the last 5 rows in the list to start compiling the 
        # data needed to calculate the standard deviation
        for row in currency_pairs[2][-5:]:
            row.add_to_running_squared_sum(curr_avg)
            
        # Calculate the standard dev using the avg
        curr_std = currency_pairs[2][-1].get_std()
            
        # Calculate the average standard dev
        if len(currency_pairs[2]) > 5:
            try:
                pop_value = currency_pairs[2][-6].std_return
            except:
                pop_value = 0
        else:
            pop_value = 0
        curr_avg_std = currency_pairs[2][-1].get_avg_std(pop_value)

            
        # -------------------Investment Strategy-----------------------------------------------
        try:
            return_value = currency_pairs[2][-1].hist_return
        except:
            return_value = 0
        if isnan(return_value) == True:
            return_value = 0

        try:
            return_value_1 = currency_pairs[2][-2].hist_return
        except:
            return_value_1 = 0
        if isnan(return_value_1) == True:
            return_value_1 = 0

        try:
            return_value_2 = currency_pairs[2][-3].hist_return
        except:
            return_value_2 = 0
        if isnan(return_value_2) == True:
            return_value_2 = 0

        try:
            upp_band = []
            for n in range(100):
                upp_band.append(currency_pairs[2][-1].avg_return + ((n+1) * 0.025 * currency_pairs[2][-1].vol_price))
                if (return_value_1 < upp_band[n] and return_value >= upp_band[n]) or (return_value_1 > upp_band[n] and return_value <= upp_band[n]) and currency_pairs[3].Prev_Action_was_Buy == True and return_value != 0: #  (return_value > 0) and (return_value_1 > 0) and  
                    currency_pairs[3].sell_curr(avg_price)
                    FD_count += 1
        except:
            pass

        try:
            low_band = []
            for n in range(100):
                low_band.append(currency_pairs[2][-1].avg_return - ((n+1) * 0.025 * currency_pairs[2][-1].vol_price))
                if (return_value_1 > low_band[n] and return_value <= low_band[n]) or (return_value_1 < low_band[n] and return_value >= low_band[n]) and currency_pairs[3].Prev_Action_was_Buy == False and return_value != 0: # and  (return_value < 0) and (return_value_1 < 0)
                    currency_pairs[3].buy_currency_pairs(avg_price)
                    FD_count += 1
        except:
            pass
            
        conn.execute(text("INSERT INTO "+currency_pairs[0]+currency_pairs[1]+"_agg1 (inserttime, maxfxrate, minfxrate, volfxrate, avgfxrate, FD) VALUES (:inserttime, :maxfxrate, :minfxrate, :volfxrate, :avgfxrate, :FD);"),[{"inserttime": last_date, "minfxrate": min_price, "maxfxrate": max_price, "volfxrate": vol_price,"avgfxrate": avg_price, "FD": FD_count}])


