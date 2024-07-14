# -*- coding: utf-8 -*-
import findspark
findspark.init()

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, avg, desc

data_path = "C:\\PySpark\\data\\movielens\\"
movies_file_path = data_path + "movies.csv"
ratings_file_path = data_path + "ratings.csv"
output_dir = data_path + "movielens_out"

spark = SparkSession \
            .builder \
            .appName("Datasorces") \
            .config("spark.master", "local") \
            .getOrCreate()

ratings_df = spark.read.format("csv")\
              .option("header", "true")\
              .option("mode", "FAILFAST")\
              .option("inferSchema", "true")\
              .load(ratings_file_path)
              
movie_df = spark.read.format("csv")\
              .option("header", "true")\
              .option("mode", "FAILFAST")\
              .option("inferSchema", "true")\
              .load(movies_file_path)              
       
#ratings_df.show()  
movie_df.show()
        
ratings_summary_df = ratings_df.groupBy("movieId") \
                     .agg(count("rating").alias("count"), avg("rating").alias("averageRating")) \
                     .where("count > 10") \
                     .orderBy(desc("averageRating")) \
                     .limit(10)
                     
#ratings_summary_df.show()
                     
joinStr = ratings_summary_df["movieId"] == movie_df["movieId"]

output = ratings_summary_df.join(movie_df, joinStr) \
           .drop(movie_df["movieId"]) \
           .select("movieId", "title", "averageRating", "count") \
           .orderBy(desc("averageRating")) \
           .coalesce(1)
           
           
output.show(truncate = False)   

output.write.format("csv").mode("overwrite").save(output_dir)          
              
spark.stop()