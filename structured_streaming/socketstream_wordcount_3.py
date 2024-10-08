#!/usr/bin/env python2
# -*- coding: utf-8 -*-

##-------------------------------------------
# Using Trigger  (processingTime='4 seconds')
##-------------------------------------------

from __future__ import print_function

import sys
import os

# setup the environment for the IDE
os.environ['SPARK_HOME'] = '/home/kanak/spark-2.4.7-bin-hadoop2.7'
os.environ['PYSPARK_PYTHON'] = '/usr/bin/python'

sys.path.append('/home/kanak/spark-2.4.7-bin-hadoop2.7/python')
sys.path.append('/home/kanak/spark-2.4.7-bin-hadoop2.7/python/lib/py4j-0.10.7-src.zip')

from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql.functions import split

if __name__ == "__main__":
    
    host = 'localhost'      # sys.argv[1]
    port = 9999             # int(sys.argv[2])
    
    spark = SparkSession\
        .builder\
        .appName("Socket Streaming")\
        .getOrCreate()
        
    spark.sparkContext.setLogLevel("ERROR")   
    spark.conf.set("spark.sql.shuffle.partitions", "1")

    # Create DataFrame representing the stream of input lines from connection to host:port
    lines = spark\
        .readStream\
        .format('socket')\
        .option('host', host)\
        .option('port', port)\
        .load()

    # Split the lines into words
    words = lines.select(
        # explode turns each item in an array into a separate row
        explode(
            split(lines.value, ' ')
        ).alias('word')
    )

    # Generate running word count
    wordCounts = words.groupBy('word').count()
    
    '''
    The trigger settings of a streaming query define the timing of streaming data 
    processing, whether the query is going to be executed as micro-batch query with 
    a fixed batch interval or as a continuous processing query. 
    
    Here are the different kinds of triggers that are supported.
    
    trigger(processingTime='1 seconds')
    trigger(once=True) 
    trigger(continuous='1 second')    
    '''
    # Start running the query that prints the running counts to the console
    query = wordCounts \
        .writeStream \
        .trigger(processingTime='4 seconds') \
        .outputMode('update') \
        .format('console') \
        .start()

    query.awaitTermination()

