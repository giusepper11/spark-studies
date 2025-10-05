"""
    docker exec -it spark-master \
    spark-submit \
    --master spark://spark-master:7077 \
    --deploy-mode client \
    --name ResourceCheckApp \
    /workspace/scripts/mod-2/pr-3.py
"""

from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .getOrCreate()
)


sc = spark.sparkContext

#print sc settings
print("Executor Memory: ", sc.getConf().get("spark.executor.memory"))
print("Driver Memory: ", sc.getConf().get("spark.driver.memory"))
print("Executor Cores: ", sc.getConf().get("spark.executor.cores"))
print("Default Parallelism: ", sc.defaultParallelism)
print("SQL Shuffle Partitions: ", sc.getConf().get("spark.sql.shuffle.partitions"))


spark.stop()