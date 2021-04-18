# Spotify Music Streaming App Data Warehouse using Amazon Redshift

## Introduction
Spotify, a music streaming app, needs to analyze it's users data to gain insights on listening habits with a aim for growing paid subscriptions. The 
app generates gigabytes of usage data daily and the business needs it presented for analysis by the analytics teams.

The data engineering team has deisgned a pipeline to move these usage data to amazon s3 storage and from there this project is to ingest it to Amazon
Redshift data warehouse via etl and denormalize the schema, build a start schema and optimize for analytics.

## Technologies

Amazon AWS S3  
Amzon AWS Redshift  
python

## Redshift Cluster Specifications
The datawarehouse utilizes a 4 node Redshift Cluster of size dc2.xlarge

## ERD Schema Design

https://github.com/patkiptoo/Amazon-AWS-Redshift-Datawarehouse-Spotify/blob/main/Relation-ERD.png


## RedShift Optimization
### Distribution Keys and Sort Keys

The songplays fact table is distributed by user_id. This ensures analysis of a given user avoid shuffling. The sort key is artist_id for optimized retrieval of an artist's songs played by a given user.
The lookup (dimension) tables have distribution style ALL. Since they aren't large comparatively, this ensures we have optimized query execution on every node of the cluster.


## ETL Pipeline

The usage data files are in S4 in json format.  
a. The song data files contain the details of the songs in the catalog along with artist and year details.  
b. The song plays details include the user details, the exact time of play, and the order of play in the session.  

The ETL process loads the S3 files into two staging tables  
1. staging_events  
2. staging_songs  

It then proceeds to load the start schema using queries defined in sql_queries.py
