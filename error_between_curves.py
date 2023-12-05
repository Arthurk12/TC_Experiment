import pandas as pd
import matplotlib.pyplot as plt
import sys
import numpy as np
import os

OUTPUT_GRAPHS_FOLDER = 'curves_difference'

if len(sys.argv) < 5 or sys.argv[1] == '-h':
    sys.stdout.write("usage: %s <file1.csv> <column_name> <file2.csv> <column_name> -g\n"%sys.argv[0])
    sys.stdout.write("-g: show the plotted graph\n")
    sys.exit(0)

def area_between_arrays(x_values, y1_values, y2_values):
    area = np.trapz(np.abs(y2_values - y1_values), x=x_values)
    return area

csv_file_name_1 = sys.argv[1]
csv_column_name_1 = sys.argv[2]
csv_file_name_2 = sys.argv[3]
csv_column_name_2 = sys.argv[4]
should_show_plotted_graph = sys.argv[5] == '-g' if len(sys.argv) == 6 else False

sanitized_filename_1 = csv_file_name_1.split('/')[-1]
sanitized_filename_2 = csv_file_name_2.split('/')[-1]

# Read the averages from the CSV file
data_1 = pd.read_csv(csv_file_name_1)[f'{csv_column_name_1}'].values
data_2 = pd.read_csv(csv_file_name_2)[f'{csv_column_name_2}'].values

min_size = min(len(data_1), len(data_2))
x = np.linspace(0, min_size, min_size)
print(f'Minimum size: {min_size} between {len(data_1)} and {len(data_2)}')
print(f'X arrray generated with len {len(x)}')

diff_area = area_between_arrays(x, data_1[:min_size], data_2[:min_size])
print(f'Difference area: {diff_area}')

if not os.path.exists(f'./{OUTPUT_GRAPHS_FOLDER}'):
  os.makedirs(f'./{OUTPUT_GRAPHS_FOLDER}')

plt.figure(figsize=(8, 6))
plt.plot(data_1, marker='o', linestyle='-', color='b')
plt.plot(data_2, marker='o', linestyle='-', color='r')
plt.fill_between(x, data_1[:min_size], data_2[:min_size], color='yellow', alpha=0.4)
plt.suptitle(f'{csv_file_name_1} x {csv_file_name_2}')
plt.title(f'Difference area: {diff_area}')
plt.xlabel('Seconds')
plt.ylabel('Average Throughput(MBps)')
plt.grid(True)
plt.savefig(f'./{OUTPUT_GRAPHS_FOLDER}/{sanitized_filename_1}x{sanitized_filename_2}.pdf', format="pdf", bbox_inches="tight")
if not should_show_plotted_graph:
  quit(0)
plt.show()