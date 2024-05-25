import pandas as pd
import requests
import json
import re
# Read user data from the Excel file
file_name='sf_users.xlsx'
user_data = pd.read_excel(file_name, sheet_name="Sheet1")  # Adjust sheet name as needed
#user_data = pd.read_excel("users.xlsx", sheet_name="Sheet1")  # Adjust sheet name as needed
# Create new columns 'user_id' and 'modified_user' with default values as None
user_data['user_id'] = None
user_data['modified_user'] = None
# Loop over all the rows in the DataFrame
for i in range(len(user_data)):
    # Get the userName from the Excel data
    user_name = user_data.loc[i, "userName"]
    # Construct the URL with the updated userName
    url = f"https://abcd1984.us-east-1.snowflakecomputing.com/scim/v2/Users?filter=userName eq \"{user_name}\""
"
    print(url)
    # Set your authorization headers (you'll need to fill in the actual headers)
    headers = {
        'Authorization': 'Bearer ver:2-hint:9050734597-did:1043-ETMsDgAAAY6gkJ2/9hqPFBorHxl6NNlk32COfgAUIMcFKtKjyABVq2pdviz+ifS+tqY='
    }
    # Make the API request
    response = requests.get(url, headers=headers)
    # Parse the response content
    response_json = json.loads(response.text)
    # Check if the response has 'Resources' key and it is not empty
    if 'Resources' in response_json and len(response_json['Resources']) > 0:
        # Get the 'id' from the response
        user_id = response_json['Resources'][0]['id']
        hidden_user_nm = response_json['Resources'][0]['userName']
        print("BEFORE", hidden_user_nm)
        # Update the 'user_id' in the DataFrame
        user_data.loc[i, 'user_id'] = user_id
    # Replace '@allscripts.com' with '@veradigm.me' in the user_name (case-insensitive)
    modified_user_name = re.sub(r'@myscripts\.com', '@acme.me', hidden_user_nm, flags=re.IGNORECASE)
    print("AFTER", modified_user_name)
    # Construct the payload with the updated userName
    payload = json.dumps({
        "schemas": [
            "urn:ietf:params:scim:api:messages:2.0:PatchOp"
        ],
        "Operations": [
            {
            "op": "replace",
            "value": {
                "userName": modified_user_name
            }
            }
        ]
        })
    #payload = json.dumps({
    #    "schemas": [
    #        "urn:ietf:params:scim:schemas:core:2.0:User",
     #       "urn:ietf:params:scim:schemas:extension:2.0:User"
     #   ],
     #   "userName": modified_user_name  # Change to this username
     #   #"active": True
    #})
    # Make a PUT request to update the user using the new URL
    put_url = f"https://abcd1984.us-east-1.snowflakecomputing.com/scim/v2/Users/{user_id}"
    #response = requests.request("PUT", put_url, headers=headers, data=payload)
    response = requests.request("PATCH", put_url, headers=headers, data=payload)
    # Append the user id & modified user to the new column
    user_data.loc[i, 'user_id'] = user_id
    user_data.loc[i, 'modified_user'] = modified_user_name
    user_data.loc[i, 'hidden_user_nm'] = hidden_user_nm
# Now user_data contains the updated information
print(f"Number of modified users: {len(user_data[user_data['modified_user'].notna()])}")
print(user_data)
# Save the updated DataFrame back to the Excel file
user_data.to_excel(file_name, sheet_name="Sheet1", index=False)