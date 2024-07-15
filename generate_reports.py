import pandas as pd
import os

device_id = '08BEAC252B9A' # the device id of the data fetched
input_file_path = f'{device_id}_PM.csv' # an empty csv file with the same name must be created(include path)
danger_thresh_file_path = f'{device_id}_danger_threshold_report.csv'
daily_file_path = f'{device_id}_daily_report.csv'
input_file_empty = os.stat(input_file_path).st_size == 0
danger_thresh_file_empty = os.stat(danger_thresh_file_path).st_size == 0
daily_file_empty = os.stat(daily_file_path).st_size == 0
#  Detect when PM2.5 goes above 30
if input_file_empty:
    print("File not found")
else:
    df= pd.read_csv(input_file_path)
    df_threshold = df[df['s_d0']>30.0][['gps_lat','gps_lon','gps_num','s_d0','timestamp']]
    print("----------Danger threshold report -----------\n")
    print(df_threshold,"\n")
    df_threshold.to_csv(danger_thresh_file_path,mode='w')

# Find daily maximum, minimum and average of PM2.5 levels
max_df = df.groupby(pd.to_datetime(df['timestamp']).dt.strftime("%d-%m-%Y")).max(['s_d0'])
min_df = (df.groupby(pd.to_datetime(df['timestamp']).dt.strftime("%d-%m-%Y")).min(['s_d0']))
mean_df = (df.groupby(pd.to_datetime(df['timestamp']).dt.strftime("%d-%m-%Y")).mean(['s_d0'])).round(3)

# Joining the 3 dataframes together to create a single report
final_df = max_df.merge(min_df,how = 'inner',on = 'timestamp').merge(mean_df,how = 'inner',on='timestamp')[['gps_lat','gps_lon','s_d0_x','s_d0_y','s_d0']]
final_df.rename(columns={"s_d0_x": "s_d0_max", "s_d0_y": "s_d0_min","s_d0":"s_d0_mean"},inplace=True)
print("-----------Daily report---------")
print(final_df)
if input_file_empty:
    print("File not found")
else:
    final_df.to_csv(daily_file_path,mode='w')
