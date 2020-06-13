# Data-Modelling-with-Cassandra

<b>Introduction:</b>
    
A startup wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. There is no easy way to query the data to generate the results, since the data reside in a directory of CSV files on user activity on the app. Here we have created an Apache Cassandra database which can create queries on song play data to answer the questions.

<b>Project Overview:</b>

In this project, we would be applying Data Modeling with Apache Cassandra and complete an ETL pipeline using Python that transfers data from a set of CSV files within a directory to create a streamlined CSV file to model and insert data into Apache Cassandra tables.

<b>Datasets:</b>

For this project, we have one dataset: event_data. The directory of CSV files partitioned by date. Here are examples of filepaths to two files in the dataset:

event_data/2018-11-08-events.csv

event_data/2018-11-09-events.csv

<b>Modelling NoSQL Database or Apache Cassandra Database and building ETL Pipeline:</b>
    
1.	Design tables to answer the queries
2.	Write Apache Cassandra CREATE KEYSPACE and SET KEYSPACE statements
3.	Write CREATE statements for each of the tables to address each queries
4.	Load the data with INSERT statement for each of the tables
5.	Included IF NOT EXISTS clauses in CREATE statements to create tables only if the tables do not already exist. We have also included DROP TABLE statement for each table, so that we can run drop and create tables whenever we want to reset our database and test our ETL pipeline
6.	Test by running the proper select statements with the correct WHERE clause

<b>Files:</b>

<b>etl.ipynb:</b> This is the final file provided in which all the queries have been written with importing the files, generating a new csv file and loading all csv files into one. All verifying the results whether all tables had been loaded accordingly as per requirement

<b>event_datafile_new.csv:</b> This is the final combination of all the files which are in the folder event_data

<b>event_Data Folder:</b> Each event file is present separately, so all the files would be combined into one into event_datafile_new.csv
