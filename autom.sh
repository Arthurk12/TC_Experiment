#!/bin/bash

source_files=(
  "report_bicycle_0001.log"
  "report_bus_0001.log"
  "report_car_0001.log"
  "report_foot_0001.log"
  "report_train_0001.log"
  "report_tram_0001.log"
)

bucket_sizes=(
  "5"
  "10"
  "15"
  "20"
  "25"
  "30"
)

SOURCE_FOLDER="original_datasets"

echo "------------Generating auxiliary data sets------------"
for file in "${source_files[@]}"
do
  for bucket_size in "${bucket_sizes[@]}"
  do
    echo 'Executing command: sudo python3 aux_dataset_generator.py "'"${SOURCE_FOLDER}/${file}"'" "'"$bucket_size"'" "'"${file%.log}_${bucket_size}.csv"'"'
    python3 aux_dataset_generator.py "${SOURCE_FOLDER}/${file}" "$bucket_size" "${file%.log}_${bucket_size}.csv"
  done
done
echo "------------Finished auxiliary data sets------------"

read -p "Press Enter to start probing TC constraints..."
mkdir ./iperf_outputs
echo "------------Probing TC constraints------------"
for file in "${source_files[@]}"
do
  for bucket_size in "${bucket_sizes[@]}"
  do
    echo 'Executing command: sudo python3 tc_switcher.py "'"aux_datasets/${file%.log}_${bucket_size}.csv"'" enp2s0 & iperf3 -c 192.168.88.241 -u -f M -b 800G -t 500 | tee "'"./iperf_outputs/iperf3_output_${file%.log}_${bucket_size}.log"'" '
    sudo ./netspeed.sh -s &&
    sudo python3 tc_switcher.py "aux_datasets/${file%.log}_${bucket_size}.csv" enp2s0 & iperf3 -c 192.168.88.241 -u -f M -b 800G -t 500 | tee "./iperf_outputs/iperf3_output_${file%.log}_${bucket_size}.log" &&
    sudo ./netspeed.sh -s &&
    sudo python3 convert_iperf3_output_to_csv.py "iperf_outputs/iperf3_output_${file%.log}_${bucket_size}.log"
  done
done
echo "------------Finished TC probing------------"

read -p "Press Enter to start calculating error for the collected data..."

echo "------------Calculating error for colected data------------"
for file in "${source_files[@]}"
do
  for bucket_size in "${bucket_sizes[@]}"
  do
    echo 'Executing command: python3  error_between_curves.py  "'"aux_datasets/${file%.log}_${bucket_size}.csv"'" Average  "'"iperf_outputs/iperf3_output_${file%.log}_${bucket_size}.log"'" Bandwidth_MBps'
    python3 error_between_curves.py "aux_datasets/${file%.log}_${bucket_size}.csv" Average "iperf_outputs/iperf3_output_${file%.log}_${bucket_size}.log.csv" Bandwidth_MBps
  done
done
echo "------------Finished calculating error------------"