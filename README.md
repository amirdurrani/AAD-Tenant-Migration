# AAD-Tenant-Migration
Customer Scenario:
Customer is migrating AAD Tenant hence migrating to a new AD Domain e.g. customer migrating from mycompany.com to acme.me.

What is this Code accomplishing:
This code is developed fro specific customer need to automate the SCIM PATCH API call to update the Username for the account objects that were modified using "ALTER USER" command within Snowflake account.

NOTE: Please modify the code to fit your needs for automating SCIM APIs to snowflake SCIM Endpoint. That is the reason I have uploaded two files with slightly different code in each one.

Step1: Import required libraries

Step2: Dump entire list of users in an excel sheet

Step3: Read user data from the Excel file

Step4: Loop over all the rows in the DataFrame

Step5: Construct the URL with the updated userName

Step6: Set your authorization headers (you'll need to fill in the actual headers)

Step7: Make the API request

Step8: Parse the response content

Step9: Check if the response has 'Resources' key and it is not empty

Step10: Get the 'id' from the response

Step11: Update the 'user_id' in the DataFrame

Step12: Replace '@mycom.com' with '@acme.me' in the user_name (case-insensitive)

Step13: Construct the payload with the updated userName

Step14: Make a PATCH request to update the user using the new URL

Step15: Save the updated DataFrame back to the Excel file
