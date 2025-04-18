from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("Get Users JSON").getOrCreate()

df_users = spark.read.json("./storage/users.jsonl")
count = df_users.count()
df_users.show(3)

spark.stop()