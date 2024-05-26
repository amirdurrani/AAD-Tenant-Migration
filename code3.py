import pandas as pd
import requests
import json
import re

# Read user data from the Excel file
user_data = pd.read_excel("users.xlsx", sheet_name="Sheet1")  # Adjust sheet name as needed

# Create a new column 'user_id' and 'modified_user' with default values as None
user_data['user_id'] = None
user_data['modified_user'] = None

# Loop over all the rows in the DataFrame
for i in range(len(user_data)):
    # Get the userName from the Excel data
    user_name = user_data.loc[i, "user_name"]

    # Construct the URL with the updated userName
    url = f"https://grb17930.us-east-1.snowflakecomputing.com/scim/v2/Users?filter=userName eq \"{user_name}\""

    # Set your authorization headers
    headers = {
        'Authorization': 'Bearer ver:2-hint:9050734597-did:1043-ETMsDgAAAY6gkJ2/ABRBRVMvQ0JDL1BLQ1M1UGFkZGluZwEAABAAEMQ5nixQw8aGa3IuK8aJ/9YAAACg/2iZMQeANQ90n7gvupoBYHW/3a5rm8Er73nbwmQ+F8G9HTkWnEDI+DIzoETst4mSO9zpInQ3xTHgcuh2eO7KCFjQrF1chAjXZEML15p+IBl8kHdXTo79ObqFcshSd4MIUefMsOQDBCOsxBQauLJo6xC7SF74sB93WT8RDXySW4EFFSNP3Y1B4r/MLeKd7q7m9hqPFBorHxl6NNlk32COfgAUIMcFKtKjyABVq2pdviz+ifS+tqY='
    }

    # Make the API request
    response = requests.get(url, headers=headers)

    # Parse the response content
    response_json = json.loads(response.text)

    # Check if the response has 'Resources' key and it is not empty
    if 'Resources' in response_json and len(response_json['Resources']) > 0:
        # Get the 'id' from the response
        user_id = response_json['Resources'][0]['id']

        # Update the 'user_id' in the DataFrame
        user_data.loc[i, 'user_id'] = user_id

    # Replace '@allscripts.com' with '@veradigm.me' in the user_name in a case-insensitive manner
    modified_user_name = re.sub(r'@allscripts\.com', '@veradigm.me', user_name, flags=re.IGNORECASE)

    # Construct the payload with the updated userName
    payload = json.dumps({
      "schemas": [
        "urn:ietf:params:scim:schemas:core:2.0:User",
        "urn:ietf:params:scim:schemas:extension:2.0:User"
      ],
      "userName": modified_user_name,  # change to this username  
      "active": True
    })

    # Make the POST request
    response = requests.request("POST", url, headers=headers, data=payload)

    # Append the modified user to the new column
    user_data.loc[i, 'modified_user'] = modified_user_name

# Save the updated DataFrame back to the Excel file
user_data.to_excel("users.xlsx", sheet_name="Sheet1", index=False)
