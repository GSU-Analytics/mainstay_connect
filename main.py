"""Example usage and demonstrations for the mainstay_connect package.

This module provides example code and demonstrations showing how to use the
MainstayConnect class to interact with the Mainstay API. It serves as both
documentation and a quick way to test your API connection.

Examples:
    Basic usage to test connection:
    
    >>> from mainstay_connect import MainstayConnect
    >>> conn = MainstayConnect()
    >>> response = conn.test_connection()
    >>> print(response)
    {'ok': True, 'org_id': 'yourOrgId', 'response_code': 200}
    
    Fetch a contact by phone number:
    
    >>> contact = conn.get_contact(id='1234567890')
    >>> print(contact['first_name'])
    'John'
    
    Get custom fields:
    
    >>> fields = conn.get_custom_fields()
    >>> print(fields['custom_fields'])
    ['Campus ID', 'Major', 'Expected Graduation']
    
    Convert API response to DataFrame:
    
    >>> contacts = conn.get_contacts(custom="Major|Computer Science")
    >>> df = conn.json_to_dataframe(contacts)
    >>> df.head()
       admithub_id  first_name  last_name  ...
    0  abc123       Jane        Doe        ...
    
Notes:
    - You'll need a valid Mainstay API token to use this module
    - The token will be requested when you first run any function
    - The token is stored securely using the keyring package
    - See the README.md for more detailed documentation
"""

from mainstay_connect import MainstayConnect

def main():
    """
    Run examples of mainstay_connect functionality.
    """
    print("Mainstay Connect Example Usage")
    print("=" * 30)
    
    # Create an instance of MainstayConnect
    print("\nInitializing connection...")
    conn = MainstayConnect()

    # Test the API connection and print the response
    print("\nTesting API connection...")
    try:
        response = conn.test_connection()
        print("Connection Test Response:", response)
    except Exception as e:
        print("Connection test failed:", e)
    
    # Example code for fetching a contact by phone number
    print("\nExample: Fetch contact by phone number")
    print("This example is commented out to prevent accidental API calls.")
    print("Uncomment the code below to test with your data:")
    print("""
    try:
        contact_response = conn.get_contact(id='1234567890')  # Replace with a valid phone number
        print("Contact Response:", contact_response)
    except Exception as e:
        print("Failed to fetch contact:", e)
    """)

    # Example code for fetching contacts with a specific custom field
    print("\nExample: Fetch contacts with a specific custom field")
    print("This example is commented out to prevent accidental API calls.")
    print("Uncomment the code below to test with your data:")
    print("""
    try:
        contacts_response = conn.get_contacts(custom="Field Name|field_value")  # Replace with your field and value
        print("Contacts Response:", contacts_response)
    except Exception as e:
        print("Failed to fetch contacts:", e)
    """)

    # Example code for retrieving custom fields
    print("\nExample: Retrieve custom fields")
    print("This example is commented out to prevent accidental API calls.")
    print("Uncomment the code below to test with your data:")
    print("""
    try:
        custom_fields_response = conn.get_custom_fields()
        print("Custom Fields Response:", custom_fields_response)
    except Exception as e:
        print("Failed to retrieve custom fields:", e)
    """)

    print("\nDocumentation and more examples can be found in the README.md file.")
    print("\nTo use the API, you'll need to have a valid Mainstay API token.")
    print("The token will be requested when you first run this or any other function,")
    print("and then stored securely using the keyring package.")

if __name__ == "__main__":
    main()