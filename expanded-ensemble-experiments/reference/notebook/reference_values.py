import os
import numpy as np
import subprocess
import shutil
import matplotlib.pyplot as plt


def get_mbar_weight_data(resultsfile):

    f = open(resultsfile, 'r')
    lines = f.readlines()
    f.close()

    weights_a = 0
    error_a = 0
    next_line = 0

    for l in lines:
        if '------------' in l:
            next_line += 1
        elif next_line is 3:
            values = l.split()
            weights_a = float(values[16])
            error_a = float(values[18])

    return weights_a, error_a


# defining the number of reference calculations
refs = ['rep_1', 'rep_2', 'rep_3', 'rep_4']

# making space for reference values
values = np.zeros(len(refs))
error = 0

# reading the reference estimates
i = 0
for r in refs:
    results_file = '../' + r + '/raw_data/results.txt'
    values[i], error = get_mbar_weight_data(results_file)
    i += 1

# calculating average and standard deviation
average = np.average(values)
std = np.std(values)

# converting to kcal/mol
conv_factor = 0.596126843592
average *= conv_factor
std *= conv_factor

# writing to file
write_file = '../raw_data/results.txt'
outfile = open(write_file, 'w')
outfile.write(str(average) + '\n')
outfile.write(str(std) + '\n')

