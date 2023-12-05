import pandas as pd
import matplotlib.pyplot as plt
import sys

if len(sys.argv) < 3 or sys.argv[1] == '-h':
    sys.stdout.write("Usage: %s <file.csv> column_name\n"%sys.argv[0])
    sys.exit(0)
  
csv_file_name = sys.argv[1]
csv_column_name = sys.argv[2]


# Read the averages from the CSV file
data = pd.read_csv(csv_file_name)

# Plotting the line chart
plt.figure(figsize=(8, 6))
plt.plot(data[f'{csv_column_name}'], marker='o', linestyle='-', color='b')
plt.title(f'{csv_file_name}')
plt.xlabel('Seconds')
plt.ylabel('Average Throughput(MBps)')
plt.grid(True)
plt.savefig(f'./{csv_file_name}.pdf', format="pdf", bbox_inches="tight")
plt.show()