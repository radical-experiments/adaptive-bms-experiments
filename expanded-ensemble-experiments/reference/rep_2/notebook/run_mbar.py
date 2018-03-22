import subprocess

# directory for alchemical analysis
alchemical_py ='/home/TravisJensen/Documents/SH2domains/Scripts/Analysis/alchemical-analysis/alchemical_analysis/alchemical_analysis.py'
subprocess.call(['python', alchemical_py, '--units', 'kBT', '-t', '300', '-d', '../raw_data/', '-p', 'CB7_Guest3', '-x', '-i', '1000'])
