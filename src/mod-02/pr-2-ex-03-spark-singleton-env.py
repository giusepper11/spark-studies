from pyspark.sql import SparkSession

class SparkManager:
    _session = None

    @classmethod
    def get_session(cls, app_name:str) -> SparkSession:
        if cls._session == None:
            cls._session = (
                SparkSession.builder
                .appName(app_name)
                .master('local[*]')
                .getOrCreate()
            )
        return cls._session
    
    @classmethod
    def stop_session(cls) -> None:
        if cls._session is not None:
            cls._session.stop()
            cls._session = None


spark = SparkManager.get_session("Restaurants Rating")


df_restaurants = spark.read.json("./storage/mysql/restaurants/01JS4W5A7YWTYRQKDA7F7N95VY.jsonl")
df_ratings = spark.read.json("./storage/mysql/ratings/01JS4W5A7YWTYRQKDA7F7N95VZ.jsonl")

df_restaurants.show(5, truncate=False)
df_ratings.show(5, truncate=False)

SparkManager.stop_session()
