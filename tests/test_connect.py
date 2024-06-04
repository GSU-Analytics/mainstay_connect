import os
import pytest
import tempfile
import pandas as pd
from mainstay_connect import MainstayConnect

@pytest.fixture
def connector():
    return MainstayConnect(service_name='MainstayConnector')

def test_load_credentials(connector):
    """Test loading credentials from the keyring."""
    token = connector.get_token()
    assert isinstance(token, str), "Token should be a string"

def test_test_connection(connector):
    """Test the API connection and confirm that the 'ok' key is in the response."""
    response = connector.test_connection()
    assert 'ok' in response, "Response should include the 'ok' key indicating success"

def test_get_contacts(connector):
    """Test fetching contacts from the Mainstay API with optional filters."""
    # Assuming the API method exists and parameters like `texting_status` and `page` are valid
    response = connector.get_contacts(texting_status="opted-in", page=1)
    assert 'results' in response
    assert isinstance(response['results'], list)
    assert len(response['results']) > 0

    # Optionally, check if the first result contains expected fields
    first_contact = response['results'][0]
    assert 'admithub_id' in first_contact
    assert 'archived' in first_contact
    assert 'can_text' in first_contact

def test_get_custom_fields(connector):
    """Test retrieving the list of valid custom fields."""
    response = connector.get_custom_fields()
    assert 'custom_fields' in response
    assert isinstance(response['custom_fields'], list)
    assert len(response['custom_fields']) > 0

def test_json_to_dataframe(connector):
    """Test converting JSON response to Pandas DataFrame."""
    json_data = connector.get_contacts(texting_status="opted-in", page=1)
    df = connector.json_to_dataframe(json_data)
    assert not df.empty
    assert 'admithub_id' in df.columns

def test_save_dataframe(connector):
    """Test saving DataFrame to a CSV file."""
    json_data = connector.get_contacts(texting_status="opted-in", page=1)
    df = connector.json_to_dataframe(json_data)

    with tempfile.TemporaryDirectory() as tmpdirname:
        file_name = 'contacts_opted_in_page_1_test.csv'
        file_path = os.path.join(tmpdirname, file_name)
        connector.save_dataframe(df, file_path)  # Pass the full path directly
        
        # Check if the file was created
        assert os.path.exists(file_path)
        
        # Optionally, read the file and check its contents
        df_loaded = pd.read_csv(file_path)
        assert not df_loaded.empty
        assert 'admithub_id' in df_loaded.columns
