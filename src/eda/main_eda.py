from .bar_chart import plot_categorical_distributions_plotly
from .bar_chart_correlation import plot_discrete_countplots_plotly
from .count_and_KDE import plot_discrete_distribution_by_target_combined
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
def main_eda():
    print("📊 Exploratory Data Analysis (EDA) started...")
    df = pd.read_csv('./data/final_processed_data.csv')

    plot_discrete_distribution_by_target_combined(df, target_col='target')
    print("✅ EDA completed successfully.")
