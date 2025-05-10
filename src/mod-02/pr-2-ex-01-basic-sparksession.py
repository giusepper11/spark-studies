from pyspark.sql import SparkSession

spark : SparkSession = (
    SparkSession.builder
    .appName('Pr 2 Ex1 - Basic session')
    .master('local[*]')
    .getOrCreate()
)

drivers_df = spark.read.json("./storage/postgres/drivers/01JS4W5A74BK7P4BPTJV1D3MHA.jsonl")

print(drivers_df.count())

drivers_df.show(5, truncate=False)

spark.stop()