import pandas as pd

class GeneralChecker:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def check_null(self):
        """Check for missing values in each column."""
        return self.df.isnull().sum()

    def check_datatype(self):
        """Return the data types of each column."""
        return self.df.dtypes

    def convert_gpa_range(self):
        """Convert raw GPA ranges to normalized format."""
        mapping = {
            '9.0 đến 10': '9-10',
            '8.0 đến cận 9.0': '8-9',
            '7.0 đến cận 8.0': '7-8',
            '6.0 đến cận 7.0': '6-7',
            '5.0 đến cận 6.0': '5-6',
            'dưới 5.0': '< 5'
        }
        self.df['last_semester_GPA'] = self.df['last_semester_GPA'].map(mapping).fillna('Unknown')

    def remove_timestamp(self):
        """Remove 'time_stamp' column if it exists."""
        if 'time_stamp' in self.df.columns:
            self.df.drop(columns=['time_stamp'], inplace=True)

    def classify_student_ranking(self, gpa_col='last_semester_GPA', conduct_col='conduct_score', new_col='new_last_semester_student_ranking'):
        """Classify student ranking based on GPA and conduct."""
        # Normalize
        self.df[gpa_col] = self.df[gpa_col].str.strip().str.replace('đến cận', '-').str.replace(' ', '')
        self.df[conduct_col] = self.df[conduct_col].str.strip().str.replace(' ', '')

        rankings = []

        for i in range(len(self.df)):
            gpa = self.df.at[i, gpa_col]
            conduct = self.df.at[i, conduct_col]

            if gpa == '9-10' and conduct == '90-100':
                rankings.append('Xuất sắc')
            elif (gpa == '8-9' and conduct in ['80-89', '90-100']) or (gpa == '9-10' and conduct == '80-89'):
                rankings.append('Giỏi')
            elif (gpa == '7-8' and conduct in ['65-79', '80-89', '90-100']) or \
                 (gpa == '8-9' and conduct == '65-79') or \
                 (gpa == '9-10' and conduct == '65-79') or \
                 (gpa == '6-7' and conduct == '80-89'):
                rankings.append('Khá')
            else:
                rankings.append('Trung bình')

        self.df[new_col] = rankings
        self.df['last_semester_student_ranking'] = self.df[new_col]
        self.df.drop(columns=new_col, inplace=True, axis=1)

    @staticmethod
    def convert_float_to_object(df: pd.DataFrame) -> pd.DataFrame:
        """
        Chuyển các cột có kiểu float64 trong DataFrame sang kiểu object (tương tự string).
        
        Args:
            df (pd.DataFrame): DataFrame đầu vào.

        Returns:
            pd.DataFrame: DataFrame đã chuyển kiểu dữ liệu.
        """
        float_columns = df.select_dtypes(include=['float64']).columns
        df[float_columns] = df[float_columns].astype('object')
        return df


    def do_all_checks(self):
        """Run all checks and transformations."""
        print("🔍 Null Checks:\n", self.check_null())
        print("🔍 Data Types:\n", self.check_datatype())
        self.convert_gpa_range()
        self.remove_timestamp()
        self.classify_student_ranking()
        self.df = self.convert_float_to_object(self.df)
        return self.df

    def get_dataframe(self):
        """Return the processed DataFrame."""
        return self.df
