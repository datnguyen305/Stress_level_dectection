import pandas as pd

class PSSCalculator:
    """
    Class to calculate PSS (Perceived Stress Scale) scores from a DataFrame.
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def _convert_columns_to_int(self):
        """
        Convert PSS question columns (1 to 10) to integer type.
        """
        for i in range(1, 11):
            col_name = str(i)
            if col_name in self.df.columns:
                self.df[col_name] = self.df[col_name].astype(int)

    def _reverse_score(self, x):
        """
        Reverse score mapping:
        0 → 4, 1 → 3, 2 → 2, 3 → 1, 4 → 0
        """
        return 4 - x

    def _apply_reverse_scoring(self):
        """
        Apply reverse scoring for positively stated questions.
        Typically PSS uses reverse scoring for questions 4, 5, 7, 8 (1-based index).
        """
        reverse_cols = ['4', '5', '7', '8']
        for col in reverse_cols:
            if col in self.df.columns:
                self.df[col] = self.df[col].apply(self._reverse_score)
                
    @staticmethod
    def convert_target(val):
        if 0 <= val < 9:
            return 0
        elif 9 <= val < 17:
            return 1
        elif 17 <= val < 25:
            return 2
        elif 25 <= val < 33:
            return 3
        else:
            return 4

    def calculate(self):
        """
        Main method to calculate the total PSS score and add it to the DataFrame.

        Returns:
            pd.DataFrame: Updated DataFrame with 'PSS Score' column.
        """
        self._convert_columns_to_int()
        self._apply_reverse_scoring()

        # Sum scores from column '1' to '10'
        pss_columns = [str(i) for i in range(1, 11) if str(i) in self.df.columns]
        self.df["target"] = self.df[pss_columns].sum(axis=1)
        self.df['target'] = self.df['target'].apply(self.convert_target)
        # Delete columns '1' to '10'
        self.df.drop(columns=pss_columns, inplace=True, axis=1)
        return self.df
