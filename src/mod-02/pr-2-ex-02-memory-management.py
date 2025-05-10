from pyspark.sql import SparkSession

spark : SparkSession = (
    SparkSession.builder
    .appName('Pr 2 Ex 2 - Memory Management')
    .master('local[*]')
    .config("spark.driver.memory", "8g")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")


drivers_df = spark.read.json("./storage/kafka/orders/01JS4W5A7XY65S9Z69BY51BEJ4.jsonl")

print(drivers_df.count())

drivers_df.show(5, truncate=False)

spark.stop()