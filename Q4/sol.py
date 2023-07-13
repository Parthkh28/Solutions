from pyspark.sql import SparkSession

# Create SparkSession
spark = SparkSession.builder \
    .appName("JSON Ingestion") \
    .getOrCreate()

# Define the path to the cloud storage folder containing the JSON files
json_folder_path = "path_to_cloud_folder_containing_json_files"

# Read JSON files using Spark Structured Streaming
df = spark.readStream \
    .format("json") \
    .schema("inferSchema") \
    .option("inferTimestamp", "true") \
    .load(json_folder_path)

# Write the ingested data to a table without any transformations
df.writeStream \
    .format("parquet") \
    .option("path", "output_table_path") \
    .option("checkpointLocation", "checkpoint_path") \
    .start()

# Start the streaming query
spark.streams.awaitAnyTermination()
