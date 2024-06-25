This readme file will help you follow along the course and execute the steps in the same order as i did. 

# 1.Create an S3 bucket and Upload the raw data to S3

Create an S3 bucket with any unique name and create a folder raw_data and Upload the data from the folder *raw_data* to your S3 bucket

# 2.Create an IAM Role (Glue Service Role) for Glue
Create a Glue Service Role in IAM with the permissions listed in this file : IAM_Roles/Glue_Service_Role.json

# 3.Create Redshift Serverless Workgroup and Namespace
Create a workgroup and namespace in Redshift Serverless as demonstrated in the video
## 3.1. Create an IAM Role for Redshift as demonstrated in the video

# 4.Create an S3 VPC Gateway Endpoint
Create S3 endpoint as demonstrated in the video

# 5.Create Glue Catalog tables for S3 data
Catalog tables are useful to explore metadata and apply ETL transformations on the columns

# 6.Create a table in Redshift using the following DDL 
CREATE TABLE joined_orders (
    order_id BIGINT,
    customer_id BIGINT,
    customer_name VARCHAR(256),
    order_date VARCHAR(256),
    total_amount DOUBLE PRECISION,
    order_item_id BIGINT ,
    product_id BIGINT,
    quantity BIGINT,
    price DOUBLE PRECISION
);


# 7.Create a data connection object for Redshift in AWS Glue
This connection object stores the connection configurations such as URL, username, password etc for Glue to connect to Redshift

