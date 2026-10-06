# Customer Churn Prediction

## Project Overview

This project predicts whether a customer is likely to churn using machine learning.

The project uses customer demographic information, services, contract details, and billing information to predict customer churn.

A Streamlit web application is also included, allowing users to enter customer details and receive a churn prediction along with the probability of churn.

---

## Dataset

The dataset contains **7,043 customer records** with information related to:

- Customer demographics
- Tenure
- Phone and internet services
- Online services
- Contract details
- Payment method
- Monthly charges
- Total charges
- Customer churn

The target variable is **Churn**.

---

## Project Workflow

The project follows these main steps:

1. Data loading and exploration
2. Exploratory Data Analysis (EDA)
3. Data preprocessing
4. Categorical variable encoding
5. Numerical feature scaling
6. Train-test split
7. Model training
8. Model evaluation
9. Hyperparameter tuning
10. Final model selection
11. Model saving using Joblib
12. Streamlit application development

---

## Machine Learning Models

The following machine learning models were evaluated:

- Logistic Regression
- Decision Tree
- Random Forest
- XGBoost

Hyperparameter tuning was performed on the main models to improve their performance.

---

## Model Evaluation

The models were evaluated using:

- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC
- Confusion Matrix

Since the main business objective is to identify customers who are likely to churn, **recall for the churn class** was given particular importance.

---

## Final Model

After model comparison and hyperparameter tuning, **Logistic Regression** was selected as the final model.

The tuned Logistic Regression model achieved approximately:

- **Accuracy:** 74%
- **Churn Recall:** 78%
- **Churn F1-score:** 62%
- **ROC-AUC:** 0.84

The model was selected because identifying customers who are likely to churn was the main business objective.

---

## Features Used

The model uses customer information such as:

- Gender
- Senior Citizen
- Partner
- Dependents
- Tenure
- Phone Service
- Multiple Lines
- Internet Service
- Online Security
- Online Backup
- Device Protection
- Tech Support
- Streaming TV
- Streaming Movies
- Contract
- Paperless Billing
- Payment Method
- Monthly Charges
- Total Charges

---

## Streamlit Application

A Streamlit web application was developed for making predictions.

The application contains two main sections:

### EDA

The EDA section displays:

- Total number of customers
- Overall churn rate
- Number of churned customers
- Number of retained customers
- Churn distribution
- Churn rate by contract type
- Churn rate by tenure
- Churn rate by monthly charges

### Predictions

The prediction section allows users to enter customer information and receive:

- Churn prediction
- Churn probability
- Risk level

The risk level is displayed as:

- Low Risk
- Medium Risk
- High Risk

---

## Project Structure

```text
Customer-Churn-Prediction/
│
├── app.py
├── churn_dataset.csv
├── churn_model.pkl
├── Customer_Churn.sql
├── customer_churn_analysis.ipynb
├── README.md
├── requirements.txt
├── .gitignore
│
└── .streamlit/
    └── config.toml 
```


## File Description

| File                            | Description                                                                                      |
| ------------------------------- | ------------------------------------------------------------------------------------------------ |
| `app.py`                        | Streamlit application for EDA and customer churn prediction                                      |
| `churn_dataset.csv`             | Customer churn dataset used for analysis and prediction                                          |
| `churn_model.pkl`               | Saved trained machine learning model and preprocessing components                                |
| `Customer_Churn.sql`            | SQL file related to the customer churn dataset                                                   |
| `customer_churn_analysis.ipynb` | Jupyter Notebook containing data analysis, preprocessing, model training, evaluation, and tuning |
| `README.md`                     | Project documentation                                                                            |
| `requirements.txt`              | Python libraries required to run the project                                                     |
| `.gitignore`                    | Specifies files and folders that should not be uploaded to GitHub                                |
| `.streamlit/config.toml`        | Streamlit theme and application configuration                                                    |


## Technologies Used

- Python – Programming language
- Pandas – Data manipulation and analysis
- NumPy – Numerical operations
- Scikit-learn – Machine learning and model evaluation
- XGBoost – Gradient boosting model
- Matplotlib – Data visualization
- Seaborn – Exploratory data visualization
- Joblib – Model saving and loading
- Streamlit – Web application development
- SQL – Data querying
- Jupyter Notebook – Data analysis and model development

## How to Run the Project

### 1. Clone the Repository

```bash
git clone https://github.com/diyatandel15/customer-churn-dashboard.git
```

Navigate to the project folder:

```bash
cd customer-churn-dashboard
```

### 2. Install the Required Libraries

Open a terminal in the project folder and run:

```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit Application

```bash
python -m streamlit run app.py
```

The application will open in your browser.

---

## Business Objective

Customer churn can lead to revenue loss for a company.

A churn prediction model can help businesses identify customers who may be likely to leave and allow them to take appropriate customer retention actions.

This project demonstrates how machine learning can be used to support customer retention decisions.

---

## Disclaimer

The prediction is based on the trained machine-learning model and is not a guarantee of actual customer behavior.