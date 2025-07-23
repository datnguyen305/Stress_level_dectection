from dotenv import load_dotenv
import os
from . import (
    rename_column,
    PSSCalculator,
    GeneralChecker,
    run_little_mcar_test,
)
from .encode_data import encode_data
from .fetch_and_store import retrieve_data, save_data
import pandas as pd

def main_preprocess():
    print("🔄 Loading environment variables...")
    load_dotenv()

    print("📥 Retrieving data from Google Drive...")
    file_id = os.getenv("FILE_ID")
    data = retrieve_data(file_id)
    print("✅ Data retrieved successfully.")

    print("🔧 Renaming columns...")
    data = rename_column(data)
    print("✅ Columns renamed.")

    print("🧠 Calculating PSS score...")
    pss_calculator = PSSCalculator(data)
    data = pss_calculator.calculate()
    print("✅ PSS score calculated.")

    print("🧪 Checking general data integrity...")
    general_checker = GeneralChecker(data)
    data = general_checker.do_all_checks()
    print("✅ Data integrity check completed.")

    print("🔎 Running MCAR test...")
    result = run_little_mcar_test(data)
    print("✅ MCAR test finished.")
    print(f"📊 MCAR Test Result: Chi2={result['chi2']}, df={result['df']}, p-value={result['p']}")
    
    print("📊 Preview of final DataFrame:")
    print(data['conduct_score'].unique())

    print("💾 Saving processed data...")
    save_data(data, file_name='./data/processed_data.csv')
    print("✅ Data saved successfully.")

    print("🔄 Encoding categorical data...")
    data, gender_map, major_map = encode_data(data)
    print("✅ Categorical data encoded.")
    data.drop(columns = 'conduct_score', inplace=True)
    print("Saving final processed data...")
    print(data.dtypes)
    save_data(data, file_name='./data/final_processed_data.csv')
    print("✅ Final processed data saved.")