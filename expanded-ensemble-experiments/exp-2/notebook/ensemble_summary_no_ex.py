import numpy as np
import glob
import os
from sklearn.metrics import mean_squared_error
from math import sqrt
import matplotlib.pyplot as plt


def get_mbar_weight_data(resultsfile):
    """
    summary: uses a log file to compute the average expanded ensemble weights after the wl-incrementor has dropped below
    a certain value

    input:
        resultsfile (string) - name of the results file to be used

    output:
        todo: decide what these are
    """

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


# collecting the weight convergence as a function of time

# simulation variables
t_steps = 29120.000  # ps

# conversion factor
factor = 0.596126843592

# defining analysis directory
analysis_dir = '../raw_data'

# defining gens and pipelines
gens = range(1, 92)

# cycling through each directory
times = None
mbar_v = None
error_v = None
diff_v = None
second = 0.0

for g in gens:
    m_f = 'results' + '.txt'
    anal_dir = analysis_dir + '/' + 'analyze_percent_' + str(g)
    mbar_data, mbar_error = get_mbar_weight_data(os.path.join(anal_dir, m_f))

    time_data = float(t_steps) * float(g)
    if times is None:
        times = time_data
        mbar_v = mbar_data
        error_v = mbar_error
        second = 1.0
    elif second == 1.0:
        times = np.append(times, time_data)
        mbar_v = np.append([mbar_v], [mbar_data], axis=0)
        error_v = np.append([error_v], [mbar_error], axis=0)
        second = 2.0
    elif second == 2.0:
        times = np.append(times, time_data)
        mbar_v = np.append(mbar_v, [mbar_data], axis=0)
        error_v = np.append(error_v, [mbar_error], axis=0)
        second = 2.0

    np.savetxt("../raw_data/results.csv", [times, mbar_v * factor, error_v * factor], delimiter=",", fmt="%10.3f")
