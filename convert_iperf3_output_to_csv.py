import re
import csv
import sys

MEGA_BYTES_TO_BYTES = 1000000

if len(sys.argv) < 2 or sys.argv[1] == '-h':
    sys.stdout.write("Usage: %s <iperf3.log>\n"%sys.argv[0])
    sys.exit(0)

iperf3_log_file_name = sys.argv[1]

def save_to_csv(bandwidth_values, output_file):
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Bandwidth_MBps'])
        for value in bandwidth_values:
            writer.writerow([value])

bandwidth_values = []

with open(iperf3_log_file_name, 'r') as file:
    for line in file:
      matches = re.search(r'(\d+\.\d+)\s+MBytes/sec\s+\d+$', line.strip())
      if matches:
          bandwidth_values.append(float(matches.group(1))*MEGA_BYTES_TO_BYTES)

save_to_csv(bandwidth_values, f'{iperf3_log_file_name}.csv')