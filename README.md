# Customer Churn Prediction with SQL

An end-to-end data science project that combines **SQL analytics**, **exploratory data analysis**, **machine learning**, and an interactive **Streamlit dashboard** to predict customer churn.


## 🚀 Live Demo
**[View Dashboard → https://diya-churn-dashboard.streamlit.app](https://diya-churn-dashboard.streamlit.app)**

## 📌 About This Project
This project solves a real business problem: identifying customers at risk of churning.
It includes data generation, SQL analysis, ML modeling, and a deployed web app.

## Project Structure

```
Customer_Churn_SQL_Project/
├── data/
│   └── customers.csv         
├── models/
│   └── churn_model.joblib     # Trained ML model
├── notebooks/
│   ├── 01_EDA.ipynb           # Exploratory data analysis
│   └── 02_Model.ipynb         # Model training & evaluation
├── src/
│   ├── generate_data.py       # Generate synthetic dataset
│   ├── train_model.py         # Train and save best model
│   └── sql_queries.sql        # 10 business SQL queries
├── app/
│   └── streamlit_app.py       # Interactive dashboard
├── requirements.txt
└── README.md
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Generate Sample Data

```bash
python src/generate_data.py
```

This creates `data/customers.csv` with 10,000 synthetic customer records.

### 3. Train the Model

```bash
python src/train_model.py
```

This trains Logistic Regression and XGBoost, compares them, and saves the best model to `data/churn_model.joblib`.

### 4. Run the Streamlit Dashboard

```bash
streamlit run app/streamlit_app.py
```

Upload a CSV or use the bundled sample data to explore EDA charts and get churn predictions.

### 5. Explore Notebooks

```bash
jupyter notebook notebooks/
```

- **01_EDA.ipynb** — Data cleaning, churn rate analysis, visualizations
- **02_Model.ipynb** — Model training, evaluation, feature importance

## Dataset Schema

| Column           | Type    | Description                          |
|------------------|---------|--------------------------------------|
| customer_id      | string  | Unique customer identifier           |
| age              | int     | Customer age (18–74)                 |
| tenure           | int     | Months as a customer (0–72)          |
| monthly_charges  | float   | Monthly billing amount               |
| total_charges    | float   | Lifetime charges                     |
| contract_type    | string  | Month-to-month / One year / Two year |
| payment_method   | string  | Payment method                       |
| churn            | int     | 1 = churned, 0 = retained            |

## SQL Queries

The file `src/sql_queries.sql` contains 10 business queries:

1. Overall churn rate
2. Churn rate by contract type
3. Average revenue from churned vs retained customers
4. Churn rate by payment method
5. High-value customers at risk
6. Tenure bucket analysis
7. Age group churn analysis
8. Monthly revenue at risk from churned customers
9. Customer lifetime value comparison
10. At-risk cohort summary

To run against a MySQL database:

```python
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine("mysql+pymysql://user:pass@localhost/churn_db")
df = pd.read_sql("SELECT * FROM customers", engine)
```

## Models

| Model                | Description                                      |
|----------------------|--------------------------------------------------|
| Logistic Regression  | Baseline linear classifier with regularization   |
| XGBoost              | Gradient boosted trees (typically best performer)|

Both models use a preprocessing pipeline with standard scaling for numeric features and one-hot encoding for categoricals.

## Dashboard Features

- **EDA Tab** — Churn distribution, contract/payment analysis, correlation heatmap
- **Predictions Tab** — Batch churn predictions with probability scores and risk levels (Low / Medium / High)
- CSV upload support with download of prediction results

## Tech Stack

- **Python** — pandas, numpy, scikit-learn, xgboost
- **Visualization** — matplotlib, seaborn, plotly
- **App** — Streamlit
- **Database** — SQLAlchemy, PyMySQL

## License

MIT
