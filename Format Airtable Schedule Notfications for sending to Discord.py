import requests

def fetch_airtable_records(base_id, table_name, token, view_name):
    # Specify the columns you want to retrieve
    fields = ["Name", "Start Time (PST)", "End Time (PST)", "Client", "Virtual Assistant", "VA Email", "Discord ID"]

    # Define the Airtable API URL
    url = f"https://api.airtable.com/v0/{base_id}/{table_name}"

    # Set up headers with the token for authentication
    headers = {
        "Authorization": f"Bearer {token}",
    }

    # Parameters for the API request
    params = {
        "fields[]": fields,  # Select specific fields
        "view": view_name,    # Specify the view name
    }

    # Make the API request to retrieve records
    response = requests.get(url, headers=headers, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        response_json = response.json()
        # Check if the response contains a 'records' key
        if "records" in response_json:
            records = response_json["records"]
            output_records = []
            for record in records:
                fields = record["fields"]
                output_records.append(fields)
            output = {"records": output_records}
        else:
            output = {"error": "Response does not contain 'records' key"}
    else:
        output = {
            "error": f"Error: {response.status_code} - {response.text}"
        }

    return output

def extract_data(records):
    extracted_data = []

    for record in records:
        va_emails = record.get("VA Email", [])  # Get the "VA Email" field, default to an empty list
        for email in va_emails:
            entry = {
                "Virtual Assistant": record.get("Virtual Assistant", ""),
                "Email": email,
                "Start Time": record.get("Start Time", ""),
                "End Time": record.get("End Time", ""),
                "Client": record.get("Client", ""),
                "Discord ID": record.get("Discord ID", "")
            }
            extracted_data.append(entry)

    return extracted_data

# Example usage:
base_id = "appniuLJAZRk6OaDn"  # Replace with your actual base ID
table_name = "tblH6ezAIX8uEam7y"  # Replace with your actual table name
token = "patUMHdDyXBjaqXku.2abb9c96acfcca70ab3c264ddbe9cdf20984bbcfa925ae04960a629264874d43"  # Replace with your actual API token
view_name = "Daily Schedule Reminder"  # Replace with the view name you want to filter on

result = fetch_airtable_records(base_id, table_name, token, view_name)

# Check for errors in the result
if "error" in result:
    print(result["error"])
else:
    # Extract data from the records
    extracted_data = extract_data(result.get("records", []))

    # Print the extracted data
    for entry in extracted_data:
        print(entry)
output = result