
import numpy as np
import matplotlib.pyplot as plt
import operator
from collections import OrderedDict

tf_idf = []
tf_idf_float = []
import csv
f = csv.reader(open("./output_table_bigrams.csv", 'rU'))
for row in f:
    print row
    tf_idf.append([row[5], row[1], row[7]])
tf_idf.remove(tf_idf[0])


for ele in tf_idf:

    pos = [x.translate(None,'[]\'') for x in ele[2].split(",")]
    noun_count = 0
    for p in pos:
        p = p.lstrip()
        p = p.rstrip()


        if p == 'NN' or p == 'NNP':
            noun_count += 1
    print noun_count, len(pos)
    if noun_count == len(pos):
        tf_idf_float.append([float(ele[0]), ele[1]])


sorted_list_dup = []
sorted_list_without_dup = []
sorted_list = sorted(tf_idf_float, key = operator.itemgetter(0))
for ele in sorted_list:
    sorted_list_dup.append(ele[1])
sorted_list_without_dup = OrderedDict.fromkeys(sorted_list_dup).keys()
print sorted_list_without_dup[:30]

'''
x_range = [x for x in range(len(tf_idf_float))]
plt.plot(x_range, tf_idf_float, 'ro')
plt.axis([0, len(tf_idf_float), 0, 2])
plt.show()
'''
