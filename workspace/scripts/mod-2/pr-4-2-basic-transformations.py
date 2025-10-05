"""
docker exec -it spark-master \
    spark-submit \
    --master spark://spark-master:7077 \
    --deploy-mode client \
    /workspace/scripts/mod-2/pr-4-2-basic-transformations.py
"""

from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col

spark = SparkSession.builder.appName("PR-4-2").getOrCreate()

restaurants_path_json = "data/mysql/restaurants/*.jsonl"

restaurant_df: DataFrame = spark.read.json(restaurants_path_json)

# Select specific columns
selected_df = restaurant_df.select("name", "city", "cuisine_type")
selected_df.show(5)

# select with cols
selected_with_cols_df = restaurant_df.select(
    col("name").alias("restaurant_name"),
    col("city"),
    col("cuisine_type"),
    col("num_reviews"),
)
selected_with_cols_df.show(5)

# Filter rows
df_high_rating = selected_with_cols_df.filter(col("num_reviews") > 1000).orderBy(
    col("num_reviews").desc()
)
df_high_rating.show(5)

spark.stop()
