'''
  This code discretizes the logs provided by gent university
  input:
    logs file: ths filename of the logs file
    buckt_size_seconds: the granularity of the discretization
    output.csv: the filename of the output csv file
  output:
    The csv file with one column containing the average throughput
    derived from the source logs. The throughput unit is bits per second.
'''

import sys
import csv
import os

MILISSECONDS_TO_SECONDS = 1000
BYTES_IN_BITS = 8
OUTPUT_FOLDER = 'aux_datasets'

if len(sys.argv) < 4 or sys.argv[1] == '-h':
    sys.stdout.write("Usage: %s <access.log> <bucket_size_seconds> <output.csv>\n"%sys.argv[0])
    sys.exit(0)
  
log_file_name = sys.argv[1]
bucket_size_seconds = int(sys.argv[2])
csv_file_name = sys.argv[3]

def extract_throughput(log_file_name=log_file_name):
  throughput = []
  with open(log_file_name, 'r') as log_file:
    for log_line in log_file:
      log_line_columns = log_line.split()
      bytes_received_since_last_report = int(log_line_columns[4])
      ms_since_last_report = int(log_line_columns[5])
      bytes_per_second = (bytes_received_since_last_report*MILISSECONDS_TO_SECONDS)/ms_since_last_report
      throughput.append(bytes_per_second)
      print("Line: bytes {}, ms {}, avg. bytes per second {}".format(bytes_received_since_last_report, ms_since_last_report, bytes_per_second))
  return throughput

def average_of_groups(vector, bucket_size):
    averages = []
    for i in range(0, len(vector), bucket_size):
        group = vector[i:i+bucket_size]
        avg = sum(group) / len(group)
        averages.extend([avg]*bucket_size)
    return averages

def write_to_csv(troughput_vector, csv_file_name=csv_file_name):
  if not os.path.exists(f'./{OUTPUT_FOLDER}'):
    os.makedirs(f'./{OUTPUT_FOLDER}')
  with open('/'.join([OUTPUT_FOLDER, csv_file_name]), 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([f'Average'])
    for avg in troughput_vector:
        writer.writerow([avg])


throughput_vector = extract_throughput()
throughput_average_vector = average_of_groups(throughput_vector, bucket_size_seconds)
print(len(throughput_vector))
print(len(throughput_average_vector))
write_to_csv(throughput_average_vector)



