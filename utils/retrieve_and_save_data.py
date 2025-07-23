from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()
file_id = os.getenv("FILE_ID")

def retrieve_data(file_id = file_id):
    """
    Retrieve data from a given ggsheet CSV_URL and return it as a pandas DataFrame.

    Parameters:
    url (str): The URL of the Google Sheets document in CSV format.
    """
    try:
        df = pd.read_excel(file_id, header=0)
        return df
    except Exception as e:
        print(f"An error occurred while retrieving data: {e}")
        return None

def save_data(data, file_name='./data/raw_data.csv'):
    """
    Save the given DataFrame to a CSV file.

    Parameters:
    data (DataFrame): The DataFrame to save.
    file_name (str): The name of the file to save the data to.
    """
    try:
        data.to_csv(file_name, index=False)
        print(f"Data saved to {file_name}")
    except Exception as e:
        print(f"An error occurred while saving data: {e}")