"""IMPORT PYTHON PACKAGES"""
# Importing the libraries
import pandas as pd
import cassandra
import re
import os
import numpy as np
import json
import csv
from cassandra.cluster import Cluster


"""CREATING LIST OF FILEPATHS TO PROCESS ORIGINAL EVENT CSV DATA FILES"""
# Checking current working directory
print(f"Current working directory : {os.getcwd()}")

# Getting current folder and subfolder event data
filepath = os.getcwd() + '/event_data'
print(filepath)

file_path_list = []

# Getting the list of file paths 
for (dirpath, dirnames, filenames) in os.walk(filepath):
        for filename in filenames:
            file_path_list.append(os.path.abspath(os.path.join(dirpath, filename)))

print(file_path_list)
print(len(file_path_list))


"""PROCESSING THE FILES TO CREATE THE DATA FILE CSV THAT WILL BE USED FOR APACHE CASSSANDRA TABLES"""
# Initiating an empty list of rows that will be generated from each file    
full_data_rows_list = [] 
    
# Looping through every filepath in the file path list 
for f in file_path_list:

# Reading csv file 
    with open(f, 'r', encoding = 'utf8', newline='') as csvfile: 
        # creating a csv reader object 
        csvreader = csv.reader(csvfile) 
        next(csvreader)
        
# Extracting each data row one by one and appending it        
        for line in csvreader:
            full_data_rows_list.append(line) 
            

print(f"Total rows : {len(full_data_rows_list)}")
print(f"Sample data:\n {full_data_rows_list[:5]}")

# Creating a smaller event data csv file called event_datafile_full.csv that will be used to insert data into Apache Cassandra tables
csv.register_dialect('myDialect', quoting=csv.QUOTE_ALL, skipinitialspace=True)

with open('event_datafile_new.csv', 'w', encoding = 'utf8', newline='') as f:
    writer = csv.writer(f, dialect='myDialect')
    writer.writerow(['artist','firstName','gender','itemInSession','lastName','length',\
                'level','location','sessionId','song','userId'])
    for row in full_data_rows_list:
        if (row[0] == ''):
            continue
        writer.writerow((row[0], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[12], row[13], row[16]))
        
        
        
# Checking the number of rows in new event csv file
with open('event_datafile_new.csv', 'r', encoding = 'utf8') as f:
    print(sum(1 for line in f))

# Making a connection to a Cassandra instance on our local machine (127.0.0.1)
try:
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()
    print("Connection Established !!")
except Exception as e:
    print(f"Connection Failed !! Error : {e}")

# Creating Keyspace    
keyspace_query = """CREATE KEYSPACE IF NOT EXISTS sparkify 
                    with REPLICATION = 
                    { 'class' : 'SimpleStrategy', 'replication_factor' : 1 }
                """
                
try:
    session.execute(keyspace_query)
except Exception as e:
    print(f"Failed to create keyspace!! Error : {e}")
    
# Setting KEYSPACE to the keyspace specified above
session.set_keyspace('sparkify')

# Creating table for query1 
create_query1 = """CREATE TABLE IF NOT EXISTS session_item (artist text, song text, length float, sessionId int, itemInSession int, PRIMARY KEY (sessionId, itemInSession))"""

try: 
    session.execute(create_query1)
    print("Table Created!!")
except Exception as e:
    print(f"Table creation failed!! Error : {e}")

# Using the event file
file = 'event_datafile_new.csv'

# Reading csv file and inserting rows into cassandra tables.
with open(file, encoding = 'utf8') as f:
    csvreader = csv.reader(f)
    next(csvreader) # skip header
    for line in csvreader:
        query = "INSERT INTO session_item (artist, song, length, sessionId, itemInSession) "
        query = query + " VALUES (%s, %s, %s, %s, %s) "
        session.execute(query, (line[0], line[10], float(line[5]), int(line[8]), int(line[3])) )
        
# SELECT statement to verify the data was entered into the table
select_query1 = "SELECT artist, song, length FROM  session_item where sessionId = 338 and itemInSession = 4"
try:
    rows = session.execute(select_query1)
except Exception as e:
    print(e)
    
for row in rows:
    print(row)
    
# Creating table for query2 
create_query2 = """CREATE TABLE IF NOT EXISTS user_session (sessionId int, userId int, artist text, song text, firstName text, lastName text, itemInSession int, PRIMARY KEY ((sessionId, userId), itemInSession)) WITH CLUSTERING ORDER BY (itemInSession ASC) """

try: 
    session.execute(create_query2)
    print("Table Created!!")
except Exception as e:
    print(f"Table creation failed!! Error : {e}")
    
# Using the event file    
file = 'event_datafile_new.csv'

# Reading csv file and inserting rows into cassandra tables.
with open(file, encoding = 'utf8') as f:
    csvreader = csv.reader(f)
    next(csvreader) # skip header
    for line in csvreader:
        query = "INSERT INTO user_session (sessionId, userId, artist, song, firstName, lastName, itemInSession) "
        query = query + " VALUES (%s, %s, %s, %s, %s, %s, %s) "
        session.execute(query, (int(line[8]), int(line[10]), line[0], line[9], line[1], line[4], int(line[3])  ) )
        
# SELECT statement to verify the data was entered into the table
select_query2 = "SELECT artist, song, firstName, lastName FROM  user_session where sessionId = 182 and userId = 10"
try:
    rows = session.execute(select_query2)
except Exception as e:
    print(e)

for row in rows:
    print(row)

# Creating table for query3
create_query3 = """CREATE TABLE IF NOT EXISTS user_song (song text, userId int, firstName text, lastName text, PRIMARY KEY ((song), userId))"""

try: 
    session.execute(create_query3)
    print("Table Created!!")
except Exception as e:
    print(f"Table creation failed!! Error : {e}")
    
# Using the event file     
file = 'event_datafile_new.csv'

# Reading csv file and inserting rows into cassandra tables.
with open(file, encoding = 'utf8') as f:
    csvreader = csv.reader(f)
    next(csvreader) # skip header
    for line in csvreader:
        query = "INSERT INTO user_song (song, userId, firstName, lastName) "
        query = query + " VALUES (%s, %s, %s, %s) "
        session.execute(query, (  line[9], int(line[10]), line[1], line[4] )  )
        
# SELECT statement to verify the data was entered into the table
select_query2 = "SELECT song, firstName, lastName FROM user_song where song = 'All Hands Against His Own'"
try:
    rows = session.execute(select_query2)
except Exception as e:
    print(e)

for row in rows:
    print(row)
    
    
    
session.execute("DROP TABLE IF EXISTS sparkify.session_item")
session.execute("DROP TABLE IF EXISTS sparkify.user_session")
session.execute("DROP TABLE IF EXISTS sparkify.user_song")



session.shutdown()
cluster.shutdown()
