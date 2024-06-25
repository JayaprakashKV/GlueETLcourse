import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame


# Initialize Glue Context
glueContext = GlueContext(SparkContext.getOrCreate())

# Parameters
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Extract data from S3 using the Data Catalog
customers = glueContext.create_dynamic_frame.from_catalog(database = "e-commerce", table_name = "customers")
orders = glueContext.create_dynamic_frame.from_catalog(database = "e-commerce", table_name = "orders")
order_items = glueContext.create_dynamic_frame.from_catalog(database = "e-commerce", table_name = "order_items")

# Convert DynamicFrames to DataFrames for joining
customers_df = customers.toDF()
orders_df = orders.toDF()
order_items_df = order_items.toDF()

# Join the data
joined_df = orders_df.join(customers_df, orders_df["customer_id"] == customers_df["customer_id"], "inner") \
    .join(order_items_df, orders_df["order_id"] == order_items_df["order_id"], "inner") \
    .select(
        orders_df["order_id"],
        orders_df["customer_id"],
        customers_df["name"].alias("customer_name"),
        orders_df["order_date"],
        orders_df["total_amount"],
        order_items_df["order_item_id"],
        order_items_df["product_id"],
        order_items_df["quantity"],
        order_items_df["price"]
    )
    
joined_df.show(5)
joined_df.printSchema()
# Transform the data
# (Add any additional transformation logic here if needed)


# Convert back to DynamicFrame
final_dynamic_frame = DynamicFrame.fromDF(joined_df, glueContext, "final_dynamic_frame")

# Load data into Redshift
glueContext.write_dynamic_frame.from_jdbc_conf(
    frame = final_dynamic_frame,
    catalog_connection = "Redshift connection",
    connection_options = {
        "dbtable": "order_summary",
        "database": "dev"
    },
    redshift_tmp_dir = "s3://glue-etl-course/tmp_dir/"
)

job.commit()
