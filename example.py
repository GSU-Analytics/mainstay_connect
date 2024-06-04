import json
import pandas as pd
from mainstay_connect import MainstayConnect

# Create an instance of MainstayConnect
conn = MainstayConnect()

# Test the API connection and print the response
response = conn.test_connection()
print("Connection Test Response:", response)

# Fetch contact by phone number
try:
    contact_response = conn.get_contact(id='4045551234')  # Assuming phone number as ID
    print("Contact Response:", contact_response)
except Exception as e:
    print("Failed to fetch contact:", e)

# Fetch contacts with a specific custom field
try:
    contacts_response = conn.get_contacts(custom="Campus ID|campusid1") # Assuming custom field as "Campus ID" and value as "campusid1
    print("Contacts Response:", contacts_response)
except Exception as e:
    print("Failed to fetch contacts:", e)

# Retrieve and print custom fields
try:
    custom_fields_response = conn.get_custom_fields()
    print("Custom Fields Response:", custom_fields_response)
except Exception as e:
    print("Failed to retrieve custom fields:", e)

# Retrieve and print custom values for a specific field
try:
    custom_values_response = conn.get_custom_values("Campus ID")
    print("Custom Values Response:", custom_values_response)
except Exception as e:
    print("Failed to retrieve custom values:", e)

# Retrieve and print campaign list by contact ID
try:
    campaign_list_response = conn.get_campaign_list(admithub_contact_id="ahd2b33d72814c61b")
    print("Campaign List Response:", campaign_list_response)
except Exception as e:
    print("Failed to retrieve campaign list:", e)

# Retrieve and print default fields
try:
    default_fields_response = conn.get_default_fields()
    print("Default Fields Response:", default_fields_response)
except Exception as e:
    print("Failed to retrieve default fields:", e)

# Retrieve and print messages for a contact
try:
    messages_response = conn.get_messages(admithub_contact_id="ahd2b33d72814c61b")
    print("Messages Response:", messages_response)

    # Optionally, save the response as a JSON file
    output_file = 'student_messages_response.json'
    with open(output_file, 'w') as f:
        json.dump(messages_response, f, indent=4)
    print(f"Response saved to {output_file}")
except Exception as e:
    print("Failed to retrieve messages:", e)
