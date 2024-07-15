import requests 
import csv
import os.path

def fetch_device_history(url,Proj_Name):
    '''Read data from the API'''
    new_data=[]
    field_names=[]
    # Fetch data from URL
    response = requests.get(url)
    results = response.json()
    total_records=results['num_of_records']
    if total_records== 0 :
        print("No data available")
    else:
        for i in range(total_records):
            result_dict = results['feeds'][0][Proj_Name][i]
            key = next(iter(result_dict)) # fetch first key in the dictionary
            new_data.append(result_dict[key]) # storing data as list of dictionaries
    # Extracting the keys of dictionary for setting field name in csv
    for k in result_dict[key].keys():
        field_names.append(k)
    return new_data,field_names

def save_data(filepath,new_data,field_names):
    '''Writing the latest data into CSV'''
    fileEmpty=os.stat(filepath).st_size == 0 # check if the csv file is empty
    with open(filepath, 'a+') as csvfile:
        writer = csv.DictWriter(csvfile,fieldnames=field_names)
        # If CSV is empty, load all the records
        if fileEmpty:
            writer.writeheader()
            writer.writerows(new_data)
        # If there is existing data in csv, append only the new records    
        else:
            # with open(filepath, 'r') as csvfile:
            csvfile.seek(0)
            csv_reader = csv.DictReader(csvfile)
            existing_data = [row for row in csv_reader]
            for l in range(len(new_data)):
                if new_data[l]['timestamp']> existing_data[-1]['timestamp'] :
                    writer.writerow(new_data[l])
    return None


device_id= '08BEAC252B9A'#'08BEAC252CE2' # Enter the required device ID
Proj_Name='AirBox'
url = f"https://pm25.lass-net.org/API-1.0.0/device/{device_id}/history/"
filepath=f'{device_id}_PM.csv' # an empty csv file with the same name must be created(include path)
new_data,field_names= fetch_device_history(url,Proj_Name)
save_data(filepath,new_data,field_names)

