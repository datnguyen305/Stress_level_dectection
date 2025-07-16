from dotenv import load_dotenv
import os 
from src.preprocess import retrieve_data, save_data, rename_column, PSSCalculator
import pandas as pd

if __name__ == "__main__":
    load_dotenv()
    file_id = os.getenv("FILE_ID")
    data = retrieve_data(file_id)
    data = rename_column(data)
    pss_calculator = PSSCalculator(data)
    data = pss_calculator.calculate()
    print(data.head())  # Display the first few rows of the DataFrame