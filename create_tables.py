# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 13:32:49 2016

@author: wangd_000

creat database for out_put
"""

import sqlite3

sqlite_file = 'SEC_out_put.db'    # name of the sqlite database file

conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

sql1='''CREATE TABLE words_date
(
date VARCHAR(15),
word VARCHAR(64),
source VARCHAR(15),
times INTEGER
) '''

c.execute(sql1)
conn.commit()

# bleow not working, don't know why
sql2='''CREATE TABLE words_value
(
word VARCHAR(64),
'1day_dow' DECIMAL(10,8),
'5days_dow' DECIMAL(10,8),
'30days_dow' DECIMAL(10,8),
'1day_nasdaq' DECIMAL(10,8),
'5days_nasdaq' DECIMAL(10,8),
'30days_nasdaq' DECIMAL(10,8),
'1day_s&p' DECIMAL(10,8),
'5days_s&p' DECIMAL(10,8),
'30days_s&p' DECIMAL(10,8),
'1day_three' DECIMAL(10,8),
'5days_three' DECIMAL(10,8),
'30days_three' DECIMAL(10,8)
) '''

c.execute(sql2)

# Committing changes and closing the connection to the database file
conn.commit()
conn.close()