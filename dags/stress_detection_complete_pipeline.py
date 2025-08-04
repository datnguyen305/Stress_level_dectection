from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os
import pandas as pd

# Add the src directory to Python path for imports
sys.path.append('/opt/airflow/src')

def load_environment_variables():
    """Load environment variables"""
    from dotenv import load_dotenv
    print("🔄 Loading environment variables...")
    load_dotenv()
    print("✅ Environment variables loaded.")

def retrieve_data_from_drive():
    """Retrieve data from local Excel file"""
    import pandas as pd
    
    print("📥 Loading data from local file...")
    # Use the existing raw data file instead of trying to download from Google Drive
    data_path = '/opt/airflow/data/raw_data.xlsx'
    
    try:
        data = pd.read_excel(data_path, header=0)
        print(f"✅ Data loaded successfully. Shape: {data.shape}")
        
        # Save to temporary location for next task
        data.to_csv('/opt/airflow/data/temp_raw_data.csv', index=False)
        print("📄 Data saved to temporary CSV file.")
        return '/opt/airflow/data/temp_raw_data.csv'
        
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        raise

def rename_columns():
    """Rename columns in the dataset"""
    sys.path.insert(0, '/opt/airflow')
    from src.preprocess.rename_columns import rename_column
    
    print("🔧 Renaming columns...")
    # Load data from previous task
    data = pd.read_csv('/opt/airflow/data/temp_raw_data.csv')
    data = rename_column(data)
    print("✅ Columns renamed.")
    
    # Save for next task
    data.to_csv('/opt/airflow/data/temp_renamed_data.csv', index=False)

def calculate_pss_score():
    """Calculate PSS score"""
    sys.path.insert(0, '/opt/airflow')
    from src.preprocess.pss_caculate import PSSCalculator
    
    print("🧠 Calculating PSS score...")
    # Load data from previous task
    data = pd.read_csv('/opt/airflow/data/temp_renamed_data.csv')
    pss_calculator = PSSCalculator(data)
    data = pss_calculator.calculate()
    print("✅ PSS score calculated.")
    
    # Save for next task
    data.to_csv('/opt/airflow/data/temp_pss_data.csv', index=False)

def check_data_integrity():
    """Check general data integrity"""
    sys.path.insert(0, '/opt/airflow')
    from src.preprocess.general_checking import GeneralChecker
    
    print("🧪 Checking general data integrity...")
    # Load data from previous task
    data = pd.read_csv('/opt/airflow/data/temp_pss_data.csv')
    general_checker = GeneralChecker(data)
    data = general_checker.do_all_checks()
    print("✅ Data integrity check completed.")
    
    # Save for next task
    data.to_csv('/opt/airflow/data/temp_checked_data.csv', index=False)

def run_mcar_test():
    """Run MCAR test"""
    sys.path.insert(0, '/opt/airflow')
    from src.preprocess.missing_data_dealing import run_little_mcar_test
    
    print("🔎 Running MCAR test...")
    # Load data from previous task
    data = pd.read_csv('/opt/airflow/data/temp_checked_data.csv')
    result = run_little_mcar_test(data)
    print("✅ MCAR test finished.")
    print(f"📊 MCAR Test Result: Chi2={result['chi2']}, df={result['df']}, p-value={result['p']}")
    
    print("📊 Preview of final DataFrame:")
    print(data['conduct_score'].unique())
    
    # Save processed data
    sys.path.insert(0, '/opt/airflow')
    from src.preprocess.fetch_and_store import save_data
    save_data(data, file_name='/opt/airflow/data/processed_data.csv')
    print("✅ Data saved successfully.")

def encode_categorical_data():
    """Encode categorical data and save final dataset"""
    sys.path.insert(0, '/opt/airflow')
    from src.preprocess.encode_data import encode_data
    from src.preprocess.fetch_and_store import save_data
    
    print("🔄 Encoding categorical data...")
    # Load processed data
    data = pd.read_csv('/opt/airflow/data/processed_data.csv')
    data, gender_map, major_map = encode_data(data)
    print("✅ Categorical data encoded.")
    
    # Drop conduct_score column
    data.drop(columns='conduct_score', inplace=True)
    print("💾 Saving final processed data...")
    print(data.dtypes)
    
    # Save final dataset
    save_data(data, file_name='/opt/airflow/data/final_processed_data.csv')
    print("✅ Final processed data saved.")
    
    return {
        'gender_mapping': gender_map,
        'major_mapping': major_map,
        'final_shape': data.shape
    }

def cleanup_temp_files():
    """Clean up temporary files"""
    import os
    temp_files = [
        '/opt/airflow/data/temp_raw_data.csv',
        '/opt/airflow/data/temp_renamed_data.csv',
        '/opt/airflow/data/temp_pss_data.csv',
        '/opt/airflow/data/temp_checked_data.csv'
    ]
    
    for file_path in temp_files:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"🗑️ Removed temp file: {file_path}")
    
    print("✅ Cleanup completed.")

# DAG configuration
default_args = {
    'owner': 'data-team',
    'start_date': datetime(2025, 8, 1),
    'catchup': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': False,
    'email_on_retry': False,
}

with DAG(
    dag_id='stress_detection_complete_pipeline',
    description='Complete stress level detection preprocessing pipeline with separate tasks',
    schedule_interval=None,  # Manual trigger
    default_args=default_args,
    tags=['stress-detection', 'preprocessing', 'complete-pipeline'],
    max_active_runs=1,
    doc_md="""
    # Complete Stress Detection Preprocessing Pipeline
    
    This DAG implements the complete preprocessing pipeline from main_preprocess.py
    with each step as a separate task for better monitoring and debugging.
    
    ## Pipeline Steps:
    1. **Load Environment**: Load environment variables and validate setup
    2. **Load Data**: Load data from local Excel file (raw_data.xlsx)
    3. **Rename Columns**: Standardize column names
    4. **Calculate PSS**: Calculate Perceived Stress Scale scores
    5. **Data Integrity**: Perform general data quality checks
    6. **MCAR Test**: Run Missing Completely At Random test
    7. **Encode Data**: Encode categorical variables
    8. **Cleanup**: Remove temporary files
    
    ## Outputs:
    - `processed_data.csv`: Intermediate processed data
    - `final_processed_data.csv`: Final encoded dataset ready for ML
    
    ## Dependencies:
    - Local raw_data.xlsx file in /opt/airflow/data/
    - All preprocessing modules in src/preprocess/
    """,
) as dag:

    # Task 1: Load environment variables
    load_env_task = PythonOperator(
        task_id='load_environment_variables',
        python_callable=load_environment_variables,
        doc_md="Load and validate environment variables",
    )

    # Task 2: Load data from local file
    retrieve_data_task = PythonOperator(
        task_id='retrieve_data_from_drive',
        python_callable=retrieve_data_from_drive,
        doc_md="Load data from local Excel file (raw_data.xlsx)",
    )

    # Task 3: Rename columns
    rename_columns_task = PythonOperator(
        task_id='rename_columns',
        python_callable=rename_columns,
        doc_md="Standardize column names in the dataset",
    )

    # Task 4: Calculate PSS score
    calculate_pss_task = PythonOperator(
        task_id='calculate_pss_score',
        python_callable=calculate_pss_score,
        doc_md="Calculate Perceived Stress Scale scores",
    )

    # Task 5: Check data integrity
    data_integrity_task = PythonOperator(
        task_id='check_data_integrity',
        python_callable=check_data_integrity,
        doc_md="Perform general data quality and integrity checks",
    )

    # Task 6: Run MCAR test
    mcar_test_task = PythonOperator(
        task_id='run_mcar_test',
        python_callable=run_mcar_test,
        doc_md="Run Missing Completely At Random statistical test",
    )

    # Task 7: Encode categorical data
    encode_data_task = PythonOperator(
        task_id='encode_categorical_data',
        python_callable=encode_categorical_data,
        doc_md="Encode categorical variables and save final dataset",
    )

    # Task 8: Cleanup temporary files
    cleanup_task = PythonOperator(
        task_id='cleanup_temp_files',
        python_callable=cleanup_temp_files,
        doc_md="Remove temporary files created during processing",
    )

    # Define task dependencies
    (load_env_task >> 
     retrieve_data_task >> 
     rename_columns_task >> 
     calculate_pss_task >> 
     data_integrity_task >> 
     mcar_test_task >> 
     encode_data_task >> 
     cleanup_task)
