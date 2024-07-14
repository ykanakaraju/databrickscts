# -*- coding: utf-8 -*-

import findspark
findspark.init()

from pyspark.sql import SparkSession, Row
from pyspark.sql.functions import expr, col, column, avg, desc, broadcast
from pyspark.sql.functions import lit, asc, count, sum
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, LongType
#from pyspark.sql.functions import count, countDistinct, sum, sumDistinct
#from pyspark.sql import SaveMode
from pyspark.sql.window import Window
from pyspark.sql.functions import max, avg, col, dense_rank, rank, row_number, to_date

spark = SparkSession \
    .builder \
    .appName("Basic Dataframe Operations") \
    .config("spark.master", "local") \
    .getOrCreate()
  





