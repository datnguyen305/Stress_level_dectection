# Stress Level Detection For UIT Undergraduates

## 📋 Project Overview 

This project builds a dataset specialize for UIT student and develops a machine learning system for detecting and classifying stress levels in individuals. With the rising concern of mental health issues, particularly stress and burnout-related incidents in Vietnam, this system aims to provide early stress detection that could potentially save lives and improve overall mental health.

### 🎯 Objectives
- Build a dataset that satisfy 5 merits: accurate, completeness, reliability, relevant, timeliness
- Develop a stress detection model using psychological and behavioral indicators.
- Implement an automated data processing pipeline using Apache Airflow
- Create a scalable solution for real-time stress level assessment
- Provide insights for mental health intervention and prevention

### 🚨 Problem Statement

Mental health challenges, including stress and burnout, have become increasingly prevalent in modern society. Recent tragic incidents in Vietnam, including cases at public venues and educational institutions, highlight the urgent need for effective stress detection and intervention systems. This project addresses the critical gap in early detection tools that could provide timely support to individuals experiencing high stress levels.

## 🏗️ Architecture

The project follows a comprehensive data science workflow:

```
Paper Survey → Data Collection → Preprocessing → Exploratory Data Analysis → Feature Engineering → Model Training → Evaluating
```

### 🛠️ Technology Stack
- **Orchestration**: Apache Airflow
- **Containerization**: Docker & Docker Compose
- **Database**: PostgreSQL
- **Data Processing**: pandas, NumPy
- **Machine Learning & Model Evaluating**: scikit-learn, AUC, ROC, F1, log-loss, DET
- **Programming Language**: Python

## 📰 Paper Survey
**News Sourcing**: Assessing the feasibility of collecting news articles from well-known Vietnamese sources such as Tuổi Trẻ, VietNamNet, and VnExpress.

**Perceived Stress Scale** [1]: Utilizing score scale to evaluate stress level of each individuals, max score = 40, the higher score means higher anxiety

**Feature Identification**:  Refer Kaggle's Student Dataset and consult with the experts.

## 📊 Data Pipeline

The data processing pipeline consists of 8 main stages:

1. **Environment Setup**: Load configuration and environment variables
2. **Data Ingestion**: Load raw survey data from Excel files
3. **Column Standardization**: Normalize column names and formats
4. **PSS Calculation**: Compute Perceived Stress Scale scores
5. **Data Validation**: Perform integrity checks and quality assurance
6. **Missing Data Analysis**: Run MCAR (Missing Completely At Random) tests
7. **Feature Encoding**: Convert categorical variables for ML compatibility
8. **Data Export**: Save processed datasets for model training

### 📁 Data Flow
```
raw_data.xlsx → processed_data.csv → final_processed_data.csv
```

## 📊 Data Analysis & Visualization

### Overall Analysis
Our comprehensive data analysis provides insights into stress patterns among UIT undergraduates:

![Overall Analysis](./photo/Overall%20Analysis.png)

*Figure 1: Comprehensive overview of stress level distribution and key demographic patterns in the UIT student dataset*

## 🚀 Getting Started

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/datnguyen305/Stress_level_dectection.git
   cd Stress_level_dectection
   ```

2. **Initialize the environment**
   ```bash
   # Run the automated setup script
   .\fix_database_fresh.bat
   ```

3. **Access Airflow UI**
   - URL: `http://localhost:8080`
   - Username: `admin`
   - Password: `admin`

### 🔧 Running the Pipeline

1. Navigate to the Airflow web interface
2. Locate the `stress_detection_complete_pipeline` DAG
3. Trigger the DAG manually or schedule it for automated runs
4. Monitor task execution and logs in real-time

## 📂 Project Structure

```
stress_level_detection/
├── dags/                          # Airflow DAG definitions
│   └── stress_detection_complete_pipeline.py
├── data/                          # Data storage
│   ├── raw_data.xlsx             # Original survey responses
│   ├── processed_data.csv        # Intermediate processed data
│   └── final_processed_data.csv  # ML-ready dataset
├── photo/                         # Analysis visualizations
│   └── Overall Analysis.png      # Comprehensive analysis overview
├── src/                          # Source code modules
│   ├── preprocess/               # Data preprocessing utilities
│   ├── eda/                      # Exploratory data analysis
│   └── utils/                    # Helper functions
├── logs/                         # Airflow execution logs
├── docker-compose.yml            # Container orchestration
├── Dockerfile                    # Custom image configuration
├── requirements.txt              # Python dependencies
└── README.md                     # Project documentation
```

## 🔬 Methodology

### Data Preprocessing
- **PSS Score Calculation**: Implementation of standardized Perceived Stress Scale
- **Data Quality Assurance**: Comprehensive validation and integrity checks
- **Missing Data Handling**: Statistical analysis using Little's MCAR test
- **Feature Engineering**: Catergorical encoding & feature correlation

### Model Development

1. **Model Selection & Hyperparameter Tuning**
   - Choose the following models: **SVC, KNN, Decision Tree, CatBoost, LightGBM**.
   - Perform hyperparameter optimization to find the best parameters for each model.

2. **Training & Evaluation**
   - Train the selected models on the dataset.
   - Evaluate using **F1-weighted** score.
   - Select the model that achieves the highest F1-weighted score.

3. **Error Analysis**
   - Analyze misclassification errors using:
     - **Log-loss**
     - **AUC-ROC**
     - **DET-Curve**

4. **Fine-tuning for Task Objective**
   - Adjust the chosen model to:
     - **Increase Recall**
     - **Decrease Precision**
   - Ensure the model aligns with the specific requirements of the problem.

5. **Retraining**
   - Retrain the fine-tuned model on the dataset.

6. **Overfitting Evaluation**
   - Assess overfitting using **Learning Curves**.




## 📈 Performance Monitoring

The Airflow pipeline provides comprehensive monitoring capabilities:
- Task-level execution tracking
- Error logging and alerting
- Data quality metrics
- Processing time optimization

## 📄 License

This project is developed for educational and research purposes. Please contact the maintainers for commercial use permissions.

## 👥 Team

- **Developer**: Nguyễn Tiến Đạt (ID: 23520262), Đặng Hoàng Gia Khiêm (ID: 23520728 ), Trần Linh Chi (ID: 22520154)
- **Institution**: VNUHCM - UIT (University of Information Technology) 
- **Course**: DS108 (Build And Preprocess Dataset), DS102 (Statistical Machine Learning)

## 🔮 Future Enhancements

- Advanced ML models (deep learning)
- Project deployment


**⚠️ Disclaimer**: This system is designed for research and educational purposes. It should not replace professional mental health assessment or treatment. If you or someone you know is experiencing mental health crisis, please contact local emergency services or mental health professionals immediately.

## References

1. Cohen, S., Kamarck, T., & Mermelstein, R. (1983). *Perceived Stress Scale*. New Hampshire Department of Administrative Services. Retrieved from [https://www.das.nh.gov/wellness/docs/percieved%20stress%20scale.pdf](https://www.das.nh.gov/wellness/docs/percieved%20stress%20scale.pdf)
2. BookingCare. (2024). *Bài test đánh giá lo âu, trầm cảm, stress DASS-21*. Retrieved from [https://bookingcare.vn/cam-nang/bai-test-danh-gia-lo-au--tram-cam--stress-dass-21-p177.html](https://bookingcare.vn/cam-nang/bai-test-danh-gia-lo-au--tram-cam--stress-dass-21-p177.html)
