"""
docker exec -it spark-master \
    spark-submit \
    --master spark://spark-master:7077 \
    --deploy-mode client \
    /workspace/scripts/mod-2/pr-4-1.py
"""

from pyspark.sql import SparkSession, DataFrame

spark = SparkSession.builder.appName("PR-4-1").getOrCreate()

resturants_path_json = "data/mysql/restaurants/*.jsonl"

restaurant_df: DataFrame = (
    spark.read.option("multiline", "true")
    .option("mode", "PERMISSIVE")
    .json(resturants_path_json)
)

print("Schema of the DataFrame:")
restaurant_df.printSchema()

spark.stop()
