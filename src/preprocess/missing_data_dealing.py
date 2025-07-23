import numpy as np
import pandas as pd
from scipy.stats import chi2

def run_little_mcar_test(data: pd.DataFrame):
    """
    Little's MCAR test implementation.
    Removes columns with missing values after the test.
    """
    df = data.copy()
    missing_cols = df.columns[df.isnull().any()]
    df = df[missing_cols]

    patterns = df.isnull().astype(int)
    pattern_strs = patterns.apply(lambda row: ''.join(row.astype(str)), axis=1)
    groups = df.groupby(pattern_strs)

    means = df.mean()
    cov = df.cov()
    inv_cov = np.linalg.pinv(cov)

    chi_square = 0
    df_total = 0

    for _, group in groups:
        n_g = group.shape[0]
        mean_g = group.mean()
        diff = (mean_g - means).fillna(0).infer_objects(copy=False).values
        stat = n_g * diff.T.dot(inv_cov).dot(diff)
        chi_square += stat
        df_total += len(diff[~np.isnan(diff)])

    # ✅ Xóa các cột bị thiếu ra khỏi DataFrame gốc
    data.drop(columns=missing_cols, inplace=True)

    return {"chi2": chi_square, "df": df_total, "p": 1 - chi2.cdf(chi_square, df_total)}
