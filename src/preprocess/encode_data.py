from sklearn.preprocessing import LabelEncoder

def encode_data(df):
    df = df.copy()

    # Label Encoding cho 'gender' và 'major'
    encoder_gender = LabelEncoder()
    encoder_major = LabelEncoder()

    df['gender'] = encoder_gender.fit_transform(df['gender'])
    df['major'] = encoder_major.fit_transform(df['major'])

    # Các mapping giá trị rời rạc
    replacements = {
        'conduct_score': {'<50': 0, '50-64': 1, '65-79': 2, '80-89': 3, '90-100': 4},
        'last_semester_GPA': {'<5': 0, '5-6': 1, '6-7': 2, '7-8': 3, '8-9': 4, '9-10': 5},
        'last_semester_student_ranking': {'Trung bình': 0, 'Khá': 1, 'Giỏi': 2, 'Xuất sắc': 3},
        'self_study_hours': {'< 1': 0, '1 - 2': 1, '2 - 3': 2, '3 - 4': 3, '> 4': 4},
        'amount_hours_spent_on_social_media': {'< 2h': 0, '2 - 5h': 1, '5 - 7h': 2, '> 7h': 3},
        'average_time_spent_sleeping': {'< 5': 0, '5 - 6.9': 1, '7 - 9': 2, '> 9': 3},
        'class_attendance_percent': {'< 20%': 0, '20 - 50': 1, '50 - 80': 2, '80 - 100': 3}
    }

    for col, mapping in replacements.items():
        df[col] = df[col].replace(mapping)

    df = df.infer_objects(copy=False)

    # Trả lại thêm cả encoder mapping
    gender_mapping = dict(zip(encoder_gender.classes_, encoder_gender.transform(encoder_gender.classes_)))
    major_mapping = dict(zip(encoder_major.classes_, encoder_major.transform(encoder_major.classes_)))

    for col in df.columns:
        df[col] = df[col].astype('int64')

    return df, gender_mapping, major_mapping
