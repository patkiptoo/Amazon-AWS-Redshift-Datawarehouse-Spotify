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

![Relation-ERD](https://user-images.githubusercontent.com/12589508/115133308-2d317b00-9fd5-11eb-9d9d-dc429fb785f9.png)



## RedShift Optimization
### Distribution Keys and Sort Keys

The songplays fact table is distributed by user_id. This ensures analysis of a given user avoid shuffling. The sort key is artist_id for optimized retrieval of an artist's songs played by a given user.
The lookup (dimension) tables have distribution style ALL. Since they aren't large comparatively, this ensures we have optimized query execution on every node of the cluster.


## Explantion of files in the repository

### create_tables.py
Creates the staging and dimension and fact tables. It drops the tables if they exists before creating.

### dwh.cfg
Holds connect and role details needed to access S3 and Redshift cluster. Certain fields blanked out for security.

### etl.py
Executes the load of the staging tables from S3 and the inserts into the dimension and fact tables.

### sql_queries.py
Construct of the necessary SQL to be used by etl.py and create_tables.py.

## How to run
Create a Redshift Cluster in AWS
Create an iam role and attach S3ReadOnly policy to the role.
Ensure you have access to the redshift cluster from within the VPC or open access through the network security group as appropriate.
Populate dwh.cfg with details of your redshift cluster and iam role.
From a terminal client with python 3 execute as follows.
$ python ./create_tables.py
$ python ./etl.py

Use the AWS Redshift Query Editor to validate the datawarehouse loaded as expected.
