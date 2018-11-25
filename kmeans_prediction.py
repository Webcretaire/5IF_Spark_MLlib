# -*- coding: utf-8 -*

import sys
from timeit import default_timer as timer

from numpy import array
from pyspark.mllib.clustering import KMeansModel
from pyspark.sql import SparkSession

if len(sys.argv) != 4:
    sys.exit('Incorrect call')

print('\n ====== Predicting ' + sys.argv[1] + ' clusters ====== \n')

spark = SparkSession.builder.appName('spark_benchmark').getOrCreate()
sc = spark.sparkContext
sc.setLogLevel('ERROR')  # By default spark displays a lot of information, we limit it to errors

# Load and parse the data
data = sc.textFile("data/household_power_consumption_no_head_no_date_prediction.csv")
parsedData = data.map(lambda line: array([float(x) for x in line.split(';')]))

finalData = sc.parallelize(parsedData.take(int(sys.argv[1]))).repartition(360)

model = KMeansModel.load(sc, "models/" + sys.argv[2])

start = timer()

# Build the model (cluster the data)
predictions = model.predict(finalData)

end = timer()

WSSSE = model.computeCost(finalData)
print("Within Set Sum of Squared Error = " + str(WSSSE))

out = open('out/learning.csv', 'a')
out.write(repr(end - start) + ' ' + repr(WSSSE) + ' ')

out.flush()
out.close()
