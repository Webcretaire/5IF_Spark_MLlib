# -*- coding: utf-8 -*

# Usage : python3 supervise_prediction.py <algorithm> <quantization> <total> <safety> <model> <url>
# Where :
#   * algorithm = python file that contains the algorithm to benchmark
#   * quantization = increment in vector count for each iteration
#   * total = total number of vectors to process at the last iteration (should be a multiple of quantization)
#   * safety = number of repetitions for each step
#   * model = name of the model to use in the model folder
#   * url = adress of the master node
#   * input_file = path of the file containing input data
# Ex : python3 supervise_prediction.py kmeans_prediction.py 20000 500000 3 KMeansModel1500000 localhost data/input.txt

import subprocess
import sys

if len(sys.argv) != 8:
    sys.exit('Incorrect call')

algorithm = sys.argv[1]
quantization = sys.argv[2]
total = sys.argv[3]
safety_arg = sys.argv[4]
model = sys.argv[5]
url = sys.argv[6]
data_file = sys.argv[7]

safety_limit = int(safety_arg)
prediction_quant = int(quantization)
prediction_max = int(total)


def append(text):
    out_file = open('out/prediction.csv', 'a')
    out_file.write(text)
    out_file.flush()
    out_file.close()


out = open('out/prediction.csv', 'w')
out.write('size ')
for i in range(0, safety_limit):
    out.write('time' + repr(i) + ' ')
out.write('\n')
out.flush()
out.close()

i = prediction_quant

while i <= prediction_max:
    append(repr(i) + ' ')

    for safety in range(0, safety_limit):
        subprocess.call(
            ["spark-submit",
             "--master", "spark://" + url + ":7077",
             "--executor-memory", "90G",
             algorithm,
             data_file,
             repr(i),
             model]
        )

    i += prediction_quant

    append('\n')
