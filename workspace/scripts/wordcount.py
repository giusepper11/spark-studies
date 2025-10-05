from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, col, lower, regexp_replace
import os
import argparse


def main(input_path: str, output_path: str, output_format: str = "parquet"):
    spark = SparkSession.builder.appName("WordCount").getOrCreate()

    # Read the input text file (each line is a record)
    df = spark.read.text(input_path)

    # Basic processing:
    #  - remove punctuation / non-word characters
    #  - split lines into words
    #  - explode into individual words
    #  - lowercase
    #  - filter out empty strings
    words = df.select(
        explode(
            split(regexp_replace(lower(col("value")), r"[^a-z0-9\s]", " "), r"\s+")
        ).alias("word")
    ).filter(col("word") != "")

    # Count occurrences
    wordcounts = words.groupBy("word").count().orderBy(col("count").desc())

    # Show top results
    wordcounts.show(20, truncate=False)

    # Write output
    output_full = output_path  # expecting full path inside container
    if output_format.lower() == "csv":
        wordcounts.coalesce(1).write.mode("overwrite").option("header", "true").csv(
            output_full
        )
    else:
        wordcounts.write.mode("overwrite").parquet(output_full)

    spark.stop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_path", required=True, help="Full path to input text file"
    )
    parser.add_argument(
        "--output_path", required=True, help="Full path to write output"
    )
    parser.add_argument(
        "--format",
        default="parquet",
        help="Output format: parquet or csv (default parquet)",
    )
    args = parser.parse_args()

    main(args.input_path, args.output_path, args.format)
