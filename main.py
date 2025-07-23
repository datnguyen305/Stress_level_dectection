# main.py
import argparse
from dotenv import load_dotenv
import os

from src.preprocess import main_preprocess
from src.eda import main_eda

def run(config):
    load_dotenv()

    if config == "preprocess":
        print("🔧 Running Preprocessing...")
        main_preprocess()
        print("✅ Preprocessing done.")
    elif config == "eda":
        print("📊 Running EDA...")
        main_eda()
        print("✅ EDA done.")
    else:
        print("❌ Unknown config. Use 'preprocess' or 'eda'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run different flows in the project.")
    parser.add_argument('--config', type=str, required=True, help="Specify flow to run: preprocess | eda")

    args = parser.parse_args()
    run(args.config)