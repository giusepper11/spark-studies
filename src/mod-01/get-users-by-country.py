from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder.appName("Get Users JSON").getOrCreate()

df_users = spark.read.json("./storage/users.jsonl")
df_users = (
    df_users.select("country")
    .groupBy("country")
    .count()
    .orderBy(col("count").desc())
    .limit(10)
)
df_users.show()

spark.stop()
