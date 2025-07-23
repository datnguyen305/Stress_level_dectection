new_columns_name = ['time_stamp', 'gender', 'academic_year', 'major', 'class_attendance_percent', 'last_semester_GPA', 'conduct_score', 'last_semester_student_ranking', 'self_study_hours', 'activity_engagement_level', 'internet_adaptation', 'amount_hours_spent_on_social_media', 'average_time_spent_sleeping', 'workout_rate', 'peer_pressure_rate', 'sharing_frequency', 'family_affects', 'family_allowance_sufficiency', 'family_educational_level', 'family_major_support', '1','2','3','4','5','6','7','8','9','10']
import pandas as pd
def rename_column(df: pd.DataFrame) -> pd.DataFrame: 
    df.columns = new_columns_name
    return df
