# PM2.5_API_ETL

The repo has python program which reads data from the public API PM2.5 Open Data for the '/device/<device_id>/history/' endpoint and stores as CSV. The fetch_data.py file has two functions where fetch_device_history() reads the past 7 days data from the public API for a given device. The second function save_data() stores the extracted data as CSV locally in the same path as the python file, named after the deviceid. The python file when run at any point in time, appends the latest data into the CSV( maximum of past 7 days).

The generate_reports.py file reads the saved CSV for the device, to generate the following:
1. A danger threshold CSV which shows the times when PM 2.5 level went above danger threshold of 30.
2. A report which stores daily average, maximum and minimum for PM 2.5 level for each day in the saved CSV.