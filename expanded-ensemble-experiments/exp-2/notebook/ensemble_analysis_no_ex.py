import os
import numpy as np
import subprocess
import shutil
import matplotlib.pyplot as plt


def get_mbar_weight_data(resultsfile):

    f = open(resultsfile, 'r')
    lines = f.readlines()
    f.close()

    weights_a = np.zeros([32])
    next_line = 0
    state = 1

    for l in lines:
        if '------------' in l:
            next_line += 1
        elif next_line is 2:
            values = l.split()
            delta = float(values[18])
            weights_a[state] = weights_a[state - 1] + delta
            state += 1

    return weights_a


def make_truncated_dhdl(dhdl_full_name, wl_min_time, wl_max_time):
    # read dhdl lines
    outfile = open('trunc_dhdl.xvg', 'w')
    with open(dhdl_full_name) as infile:
        for line in infile:
            if line[0] is '@':
                outfile.write(line)
            elif line[0] is '#':
                outfile.write(line)
            else:
                line_temp = line.split()
                time = float(line_temp[0])
                if time > wl_min_time:
                    if time < wl_max_time:
                        outfile.write(line)

    return


def get_average_weight_data(logfile, time_min, time_max):
    """
    summary: uses a log file to compute the average expanded ensemble weights after the wl-incrementor has dropped below
    a certain value

    input:
        logfile (string) - name of the log file to be used
        wl_max (float) - wl-incrementor value to collect data after

    output:
        todo: decide what these are
    """

    f = open(logfile, 'r')
    lines = f.readlines()
    f.close()

    wldelta = None
    time = None
    step = None
    next_line = 0
    weight_line = 0
    wl_max_hit = 0
    wl_max_step = None
    wl_max_time = None
    weights_a = np.zeros([32])
    wl_max = 100
    count = 0
    for l in lines:
        if 'Step           Time         Lambda' in l:
            next_line = 1
        elif 'Wang-Landau incrementor' in l:
            vals = l.split(':')
            if wldelta is None:
                wldelta = map(float, vals[1].split())
            else:
                wldelta.extend(map(float, vals[1].split()))
            if wl_max_step is None:
                if wldelta is not None:
                    if float(wldelta[-1]) < float(wl_max):
                        wl_max_step = step[-1]
                        wl_max_time = time[-1]
                        wl_max_hit = 1
        elif next_line is 1:
            vals = l.split()
            if time is None:
                time = map(float, vals[1].split())
                step = map(float, vals[0].split())
            else:
                time.extend(map(float, vals[1].split()))
                step.extend(map(float, vals[0].split()))
            if float(time[-1]) > float(time_max):
                wl_max_hit = 0
            elif float(time[-1]) > float(time_min):
                wl_max_hit = 1
            next_line = 0
        elif 'N   FEPL  CoulL' in l:
            if wl_max_hit is 1:
                weight_line = 1
                count += 1
        elif weight_line is 1:
            if wl_max_hit is 1:
                vals = l.split()
                state = int(vals[0])
                weight = float(vals[6])
                if state is 32:
                    weight_line = 0
                weights_a[state-1] += weight
        else:
            next_line = 0

    weights_a /= count
    np.set_printoptions(suppress=True)
    if wl_max_time is None:
        print('error, wl-incrementor never went below %s' % wl_max)
    return weights_a


def main():
    # defining the amount of data points the simulation should be broken into and the total simulation time
    input_name = 'CB7G3'
    total_time = 29120.000  # ps  # in ps
    increments = 91  # number of data points to make
    pipes = 16  # number of pipelines
    inc_time = float(total_time / increments)

    # directory for alchemical analysis
    alchemical_py = '/home/TravisJensen/Documents/SH2domains/Scripts/Analysis/alchemical-' \
                    'analysis/alchemical_analysis/alchemical_analysis.py'

    for index in range(1, increments + 1):
        end_time = float(index) * inc_time
        start_time = end_time / 3.0
        name = str(index)
        analysis_dir = 'analyze' + '_' + 'percent' + '_' + name
        wd = '../raw_data'
        absolute_analysis_dir = wd + '/' + analysis_dir
        os.system('mkdir ' + absolute_analysis_dir)
        for pipe_index in range(1, pipes + 1):
            dhdl_full_name = wd + '/' + input_name + '_' + str(pipe_index) + '_dhdl.xvg'
            make_truncated_dhdl(dhdl_full_name, start_time, end_time)
            dhdl_trunc_full_name = wd + '/' + 'trunc_dhdl.xvg'
            newfile = input_name + '_' + str(pipe_index) + '.xvg'
            shutil.move(dhdl_trunc_full_name, absolute_analysis_dir + '/' + newfile)

        # running MBAR
        subprocess.call(['python', alchemical_py, '--units', 'kBT', '-t', '300', '-d',
                        absolute_analysis_dir, '-p', input_name + '_', '-x', '-i', '1000'])

if __name__ == "__main__":
    main()
