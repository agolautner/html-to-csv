from bs4 import BeautifulSoup
import os
import csv
import datetime

#defining the data keys to look for
data_keys = ["mac address", "ip address", "alternate tftp", "alternate tftp address", "tftp server 1", "tftp server 2"]

def extract_data_from_file(file_path):
    result = {}
    with open(file_path, 'r') as f:
        # parsing the html
        soup = BeautifulSoup(f.read(), 'html.parser')
        # finding all tables in the parsed data
        tables = soup.find_all('table')
        # looping through the tables and rows
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                tds = row.find_all('td')
                # if the size of the table matches the expected 3 columns
                if len(tds) >= 2 and tds[0].text.strip().lower() in data_keys:
                    key = tds[0].text.strip().lower()
                    value = tds[2].text.strip().lower()
                    if value:
                        # adding the key-value pair to the corresponding key in the result dictionary
                        result[key] = value
    return result

folder_path = "../za/za/"
results = {}
#looping over all files in the dictionary
for file_name in os.listdir(folder_path):
    if file_name.endswith(".html"):
        file_path = os.path.join(folder_path, file_name)
        # checking if file size is greater than 0
        if os.path.getsize(file_path) > 0:
            result = extract_data_from_file(file_path)
            # stripping the file extension for the files
            results[os.path.splitext(file_name)[0]] = result

# Writing the results to a CSV file

now = datetime.datetime.now()
timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
output_file = f"html-to-csv-{timestamp}.csv"

with open(output_file, 'w', newline='') as f:
    writer = csv.writer(f)
    # Write header row
    writer.writerow(["IP Address", "MAC Address", "Alternate TFTP", "Alternate TFTP Address", "TFTP Server 1", "TFTP Server 2"])
    # Write data rows
    for file_name, data in results.items():
        writer.writerow([
            data.get("ip address", ""), 
            data.get("mac address", ""), 
            data.get("alternate tftp", ""), 
            data.get("alternate tftp address", ""), 
            data.get("tftp server 1", ""), 
            data.get("tftp server 2", "")
        ])