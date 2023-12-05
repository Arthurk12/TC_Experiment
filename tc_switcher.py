import sys
import csv
import subprocess
import time

last_applied_constraint = None

if len(sys.argv) < 3 or sys.argv[1] == '-h':
  sys.stdout.write("Usage: %s <trace.csv> <target_interface> <max_seconds>\n"%sys.argv[0])
  sys.exit(0)

csv_trace = sys.argv[1]
target_interface = sys.argv[2]
max_seconds = int(sys.argv[3]) if len(sys.argv) == 4 else None

def apply_bandwidth_constraint(constraint_in_bytes_per_second, interface=target_interface):
  global last_applied_constraint
  if constraint_in_bytes_per_second != last_applied_constraint:
    print(f"Applying constraint: {constraint_in_bytes_per_second} bytes per second")
    apply_constraint_command = f"sudo ./netspeed.sh -l {constraint_in_bytes_per_second}bps"
    subprocess.run(apply_constraint_command, shell=True)

    last_applied_constraint = constraint_in_bytes_per_second


seconds_counter = 0

# Abre o arquivo CSV
with open(csv_trace, "r") as csvfile:
  reader = csv.reader(csvfile, delimiter=",")
  next(reader)

  # Itera sobre as linhas do arquivo
  for row in reader:
    seconds_counter+=1
    # Obtém o valor da largura de banda
    bandwidth = round(float(row[0]))

    apply_bandwidth_constraint(bandwidth)
    
    if max_seconds and seconds_counter >= max_seconds:
      break

    # Aguarda 1 segundo
    time.sleep(1)
