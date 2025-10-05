"""
    docker exec -it spark-master \
    spark-submit \
    --master spark://spark-master:7077 \
    --deploy-mode client \
    /workspace/scripts/mod-2/pr-2.py
"""

from pyspark.sql import SparkSession

spark = (
    SparkSession.builder.appName("ResourceOptimizedApp")
    .config("spark.executor.memory", "2g")
    .config("spark.driver.memory", "4g")
    .config("spark.executor.cores", "2")
    .config("spark.default.parallelism", "8")
    .config("spark.sql.shuffle.partitions", "20")
    .getOrCreate()
)

data = [("Alice", 34), ("Bob", 45), ("Cathy", 29)]
columns = ["Name", "Age"]
df = spark.createDataFrame(data, columns)
df.show()

spark.stop()
