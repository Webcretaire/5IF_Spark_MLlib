# -*- coding: utf-8 -*
import sys
from timeit import default_timer as timer

from numpy import array
from pyspark.mllib.clustering import KMeans
from pyspark.sql import SparkSession

if len(sys.argv) != 4:
    sys.exit('Incorrect call')

print("\n ====== Processing " + sys.argv[2] + " vectors ====== \n")

spark = SparkSession.builder.appName('spark_benchmark').getOrCreate()
sc = spark.sparkContext
sc.setLogLevel('ERROR')  # By default spark displays a lot of information, we limit it to errors

# Load and parse the data
data = sc.textFile(sys.argv[1])
parsedData = data.map(lambda line: array([float(x) for x in line.split(';')]))

finalData = sc.parallelize(parsedData.take(int(sys.argv[2]))).repartition(360)

start = timer()

# Build the model (cluster the data)
clusters = KMeans.train(finalData, 12, maxIterations=10, initializationMode="random")

end = timer()

# Evaluate clustering by computing Within Set Sum of Squared Errors
# def error(point):
#     center = clusters.centers[clusters.predict(point)]
#     return sqrt(sum([x ** 2 for x in (point - center)]))
#
#
# WSSSE = finalData.map(lambda point: error(point)).reduce(lambda x, y: x + y)
WSSSE = clusters.computeCost(finalData)
print("Within Set Sum of Squared Error = " + str(WSSSE))

# Save and load model
clusters.save(sc, "models/" + sys.argv[3] + sys.argv[2])
# sameModel = KMeansModel.load(sc, "models/" + sys.argv[3] + sys.argv[2])

out = open('out/learning.csv', 'a')
out.write(repr(end - start) + ' ' + repr(WSSSE) + ' ')

out.flush()
out.close()
