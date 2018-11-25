# -*- coding: utf-8 -*

f1 = open("data/household_power_consumption_no_head.csv", "r")
f2 = open("data/household_power_consumption_no_head_no_date_learning.csv", "w")
f3 = open("data/household_power_consumption_no_head_no_date_prediction.csv", "w")

dataF1 = f1.readlines()
i = 0

for line in dataF1:
    if "?" not in line:
        (f2 if i < 1500000 else f3).write(line.partition(';')[2].partition(';')[2])
        i += 1

f2.flush()
f2.close()
f3.flush()
f3.close()
f1.close()
