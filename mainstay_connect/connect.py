# connect.py

"""
This module, connect.py, provides the MainstayConnect class, which facilitates
communication with the Mainstay API. It includes methods for authenticating,
retrieving various types of data, and managing API tokens via the keyring system.

Classes:
    MainstayConnect: Handles the creation and management of connections to the Mainstay API.

Methods:
    get_token(self) -> str:
        Retrieves the API token from the keyring or prompts for it if not found.
    reset_token(self) -> None:
        Allows the user to reset the stored API token.
    test_connection(self) -> Dict[str, any]:
        Tests the API connection and returns the response including a status code.
    get_contact(self, id: str) -> Dict[str, any]:
        Fetches a specific contact from the Mainstay API based on the provided identifier.
    get_contacts(self, **filters) -> Dict[str, any]:
        Retrieves contacts from the API based on specified filter criteria.
    get_custom_fields(self) -> Dict[str, any]:
        Returns a list of custom fields defined in the Mainstay API.
    get_custom_values(self, field_name: str) -> Dict[str, any]:
        Retrieves unique values for a specified custom field from the API.
    get_campaign_list(self, **filters) -> Dict[str, any]:
        Fetches a list of campaigns from the API filtered by specified criteria.
    get_default_fields(self) -> Dict[str, any]:
        Obtains a list of default contact fields from the Mainstay API.
    get_messages(self, **filters) -> Dict[str, any]:
        Retrieves messages based on specified filtering criteria from the API.
    save_dataframe(self, df: pd.DataFrame, filepath: str) -> None:
        Saves a pandas DataFrame to a CSV file at the specified path.
    json_to_dataframe(self, json_data: Dict[str, any], key: str = 'results') -> pd.DataFrame:
        Converts JSON response data from the API into a pandas DataFrame.

Further documentation is available at:
https://docs.api.mainstay.com/
"""


import requests
import keyring
import pandas as pd
from typing import Dict, Any

class MainstayConnect:
    base_url = "https://api.admithub.com/"

    def __init__(self, service_name: str = 'MainstayConnector'):
        self.service_name = service_name
        self.token = self.get_token()
        self.headers = {"Authorization": f"APIToken {self.token}"}

    def get_token(self) -> str:
        """
        Retrieve the API token from the keyring system storage or prompt the user to enter it manually if it is not already saved.

        The method checks if a token is stored in the keyring under the given service name and the key 'api_token'.
        If the token is not found, it prompts the user to enter a token, which is then saved to the keyring for future use.

        Returns:
            str: The token to be used for API authorization.

        Example:
            >>> connector = MainstayConnect()
            >>> api_token = connector.get_token()
            >>> print(api_token)
            APIToken abcd1234xyz
        """
        token = keyring.get_password(self.service_name, 'api_token')
        if not token:
            token = input("Enter the API token: ")
            keyring.set_password(self.service_name, 'api_token', token)
        return token

    def reset_token(self) -> None:
        """
        Prompts the user to enter a new API token and stores it in the keyring.

        This method is used to update the stored API token in the keyring system storage.
        It requests the user to input a new token which is then securely saved, replacing
        the old one. It confirms the action with a success message upon completion.

        Returns:
            None

        Example:
            >>> connector = MainstayConnect()
            >>> connector.reset_token()
            Enter the new API token: abc12345xyz
            Token has been reset successfully.
        """
        new_token = input("Enter the new API token: ")
        keyring.set_password(self.service_name, 'api_token', new_token)
        print("Token has been reset successfully.")

    def test_connection(self) -> Dict[str, any]:
        """
        Tests the connection to the Mainstay API using the provided URL and headers.

        This method attempts to authenticate with the Mainstay API to ensure that the current
        API token is valid. It appends the HTTP status code to the response data, which helps
        in identifying connection issues.

        Returns:
            Dict[str, any]: A dictionary containing the JSON response from the API, including
                            a 'response_code' key with the HTTP status code of the request.

        Example:
            >>> connector = MainstayConnect()
            >>> connection_test = connector.test_connection()
            >>> print(connection_test)
            {'ok': True, 'org_id': 'georgiaRetention', 'response_code': 200}
    """
        auth_url = self.base_url + "auth_valid"
        response = requests.get(auth_url, headers=self.headers)
        response_data = response.json()
        response_data['response_code'] = response.status_code
        return response_data

    def get_contact(self, id: str, **kwargs) -> Dict[str, Any]:
        """
        Retrieve a single contact by CRM ID, phone, or AdmitHub ID from the Mainstay API.

        Args:
            id (str): CRM ID, phone, or AdmitHub ID of the contact.
            **kwargs: Arbitrary keyword arguments for optional filters, such as:
                - texting_status (Optional[str]): Filter by texting status (opted-in, opted-out, temp-pause).
                - custom (Optional[str]): Filter by custom fields.
                - can_text (Optional[str]): Filter by can_text value (True, true, 1, False, false, 0).
                - include_test_contacts (Optional[str]): Include test contacts (True, true, 1, False, false, 0).
                - include_nonpermitted_contacts (Optional[str]): Include non-permitted contacts (True, true, 1, False, false, 0).
                - modified_since (Optional[str]): Filter by last modified date (ISO 8601 format).
                - modified_before (Optional[str]): Filter by modified before date (ISO 8601 format).
        
        Returns:
            dict: JSON response from the API containing the contact details.

        Example:
            >>> connector = MainstayConnector()
            >>> contact = connector.get_contact("1234567890", texting_status="opted-in")
            >>> print(contact)
            {...}
        """
        url = f"{self.base_url}contacts/{id}/"
        
        # Remove any None values from the kwargs dictionary
        params = {key: value for key, value in kwargs.items() if value is not None}
        
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return {"detail": "not found"}
        else:
            response.raise_for_status()

    def get_contacts(self, **kwargs) -> Dict[str, Any]:
        """
        Fetch contacts from the Navigate API with optional filters.
        
        Args:
            **kwargs: Arbitrary keyword arguments for optional filters, such as:
                - texting_status (Optional[str]): Filter by texting status (opted-in, opted-out, temp-pause).
                - can_text (Optional[str]): Filter by can_text value (True, true, 1, False, false, 0).
                - custom (Optional[str]): Filter by custom fields.
                - include_test_contacts (Optional[str]): Include test contacts (True, true, 1, False, false, 0).
                - include_nonpermitted_contacts (Optional[str]): Include non-permitted contacts (True, true, 1, False, false, 0).
                - modified_since (Optional[str]): Filter by last modified date (ISO 8601 format).
                - modified_before (Optional[str]): Filter by modified before date (ISO 8601 format).
                - page (Optional[int]): Page number for paginated results.
            
        Returns:
            dict: JSON response from the API containing the contacts.

        Example:
            >>> connector = NavigateConnector()
            >>> contacts = connector.get_contacts(texting_status="opted-in", page=1)
            >>> print(contacts)
            {...}
        """
        url = self.base_url + "contacts/"
        
        # Remove any None values from the kwargs dictionary
        params = {key: value for key, value in kwargs.items() if value is not None}
        
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def get_custom_fields(self) -> Dict[str, Any]:
        """
        Retrieve the list of valid custom fields from the Mainstay API.

        Returns:
            dict: JSON response from the API containing the custom fields.

        Example:
            >>> connector = MainstayConnector()
            >>> custom_fields = connector.get_custom_fields()
            >>> print(custom_fields)
            {'custom_fields': ['Field1', 'Field2', ...]}
        """
        url = self.base_url + "custom_fields"
        
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def get_custom_values(self, field: str) -> Dict[str, Any]:
        """
        Retrieve a list of unique values for a specified custom field from the Mainstay API.

        Args:
            field (str): Name of the valid, existing custom field.

        Returns:
            dict: JSON response from the API containing the unique values.

        Example:
            >>> connector = MainstayConnector()
            >>> custom_values = connector.get_custom_values("Campus")
            >>> print(custom_values)
            {'values': ['Value1', 'Value2', ...]}
        """
        url = self.base_url + "custom_values"
        
        params = {'field': field}
        
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 400:
            return {"detail": "Missing or invalid field"}
        else:
            response.raise_for_status()

    def get_default_fields(self) -> Dict[str, Any]:
        """
        Retrieve a list of default (non-custom) contact fields from the Mainstay API.

        Returns:
            dict: JSON response from the API containing the default fields.

        Example:
            >>> connector = MainstayConnector()
            >>> default_fields = connector.get_default_fields()
            >>> print(default_fields)
            {...}
        """
        url = self.base_url + "default_fields"
        
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def get_campaign_list(self, **kwargs) -> Dict[str, Any]:
        """
        Retrieve a list of campaigns from the Mainstay API with optional filters.

        Args:
            **kwargs: Arbitrary keyword arguments for optional filters, such as:
                - since (Optional[str]): Return all campaigns since this date (ISO 8601 format).
                - before (Optional[str]): Return all campaigns before this date (ISO 8601 format).
                - script (Optional[str]): Return all campaigns with scripts matching this AdmitHub campaign script ID.
                - status (Optional[str]): Return all campaigns that match this status.
                - scheduler (Optional[str]): Return all campaigns scheduled by a Mascot admin with this AdmitHub user ID.
                - show_hidden (Optional[str]): Show hidden campaigns (True, true, 1).
                - show_test (Optional[str]): Show test campaigns (True, true, 1).
                - crm_id (Optional[str]): Return all campaigns for which a contact with the provided CRM ID was a recipient.
                - admithub_contact_id (Optional[str]): Return all campaigns for which a contact with the provided AdmitHub ID was a recipient.
                - page (Optional[int]): A page number within the paginated result set.
        
        Returns:
            dict: JSON response from the API containing the campaigns.

        Example:
            >>> connector = MainstayConnector()
            >>> campaigns = connector.get_campaign_list(status="completed", page=1)
            >>> print(campaigns)
            {...}
        """
        url = self.base_url + "campaigns/"
        params = {key: value for key, value in kwargs.items() if value is not None}
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def get_messages(self, **kwargs) -> Dict[str, Any]:
        """
        Retrieve a list of messages from the Mainstay API with optional filters.

        Args:
            **kwargs: Arbitrary keyword arguments for optional filters, such as:
                - since (Optional[str]): Return all messages created since this date (ISO 8601 format).
                - before (Optional[str]): Return all messages created before this date (ISO 8601 format).
                - admithub_contact_id (Optional[str]): Return all messages associated with a specific contact by their AdmitHub ID.
                - admithub_id (Optional[str]): Filter messages based on the AdmitHub ID of the message.
                - contact_crm_id (Optional[str]): Filter messages based on the CRM ID of the contact associated with the message.
                - test_user (Optional[str]): Filter messages based on the test_user status of the sender.
                - include_test_user (Optional[str]): Include messages from test contacts.
                - page (Optional[int]): A page number within the paginated result set.
        
        Returns:
            dict: JSON response from the API containing the messages.

        Example:
            >>> connector = MainstayConnector()
            >>> messages = connector.get_messages(admithub_contact_id="dvvvvq9dd9450a9", page=1)
            >>> print(messages)
            {...}
        """
        url = self.base_url + "messages/"
        params = {key: value for key, value in kwargs.items() if value is not None}
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def json_to_dataframe(self, json_data: Dict[str, Any], key: str = 'results') -> pd.DataFrame:
        """
        Convert JSON response to a Pandas DataFrame.

        Args:
            json_data (dict): JSON response from the API.
            key (str): Key in the JSON data to extract the data from.

        Returns:
            pd.DataFrame: DataFrame containing the data.

        Example:
            >>> connector = MainstayConnector()
            >>> json_data = connector.get_contacts(texting_status="opted-in", page=1)
            >>> df = connector.json_to_dataframe(json_data)
            >>> print(df.head())
        """
        if key in json_data:
            data = json_data[key]
            return pd.DataFrame(data)
        else:
            return pd.DataFrame()

    def save_dataframe(self, df: pd.DataFrame, filepath: str):
        """
        Save the DataFrame to a CSV file at the specified filepath.

        Args:
            df (pd.DataFrame): DataFrame to save.
            filepath (str): Full path to the file where the DataFrame should be saved.
        """
        df.to_csv(filepath, index=False)