# data_loader.py
import pandas as pd
from sklearn.model_selection import train_test_split
from config import SEED, CSV_PATH

def load_and_split_data():
    df = pd.read_csv(CSV_PATH)
    X = df.drop(columns=['target'])
    y = df['target']

    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.4, random_state=SEED)
    X_dev, X_test, y_dev, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=SEED)

    return X_train, X_dev, X_test, y_train, y_dev, y_test, df
