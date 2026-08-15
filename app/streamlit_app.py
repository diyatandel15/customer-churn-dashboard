"""
Streamlit dashboard for Customer Churn Prediction.
Run: streamlit run app/streamlit_app.py
"""

import os
import sys

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st


# Project root for model path resolution
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(PROJECT_ROOT, "data", "churn_model.joblib")

NUMERIC_FEATURES = ["age", "tenure", "monthly_charges", "total_charges"]
CATEGORICAL_FEATURES = ["contract_type", "payment_method"]
REQUIRED_COLUMNS = ["customer_id"] + NUMERIC_FEATURES + CATEGORICAL_FEATURES

st.set_page_config(
    page_title="Diya's Customer Churn Dashboard",
    page_icon="📊",
    layout="wide",
)
# --- NEW HEADER WITH LOGO ---
col1, col2 = st.columns([1, 5])

with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/2991/2991148.png", width=80)

with col2:
    st.title("Diya's Customer Churn Dashboard")
    st.markdown("**Predict which customers are at risk of leaving**")
    st.markdown("---")
# --- END HEADER ---


@st.cache_resource
def load_model():
    """Load the trained churn model from disk."""
    if not os.path.exists(MODEL_PATH):
        st.error(f"Model not found at `{MODEL_PATH}`. Run `python src/train_model.py` first.")
        st.stop()
    return joblib.load(MODEL_PATH)


def validate_columns(df: pd.DataFrame) -> bool:
    """Check that uploaded CSV has all required columns."""
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        st.error(f"Missing columns: {', '.join(missing)}")
        return False
    return True


def render_eda(df: pd.DataFrame):
    """Render exploratory data analysis charts."""
    st.subheader("Exploratory Data Analysis")

    # KPI metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Customers", f"{len(df):,}")
    if "churn" in df.columns:
        churn_rate = df["churn"].mean() * 100
        col2.metric("Churn Rate", f"{churn_rate:.1f}%")
        col3.metric("Churned", f"{df['churn'].sum():,}")
        col4.metric("Retained", f"{(len(df) - df['churn'].sum()):,}")
    else:
        col2.metric("Avg Monthly Charges", f"${df['monthly_charges'].mean():.2f}")
        col3.metric("Avg Tenure", f"{df['tenure'].mean():.1f} mo")
        col4.metric("Avg Age", f"{df['age'].mean():.1f}")

    # Row 1: Churn distribution + contract type
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    if "churn" in df.columns:
        sns.countplot(data=df, x="churn", ax=axes[0], palette="Set2")
        axes[0].set_title("Churn Distribution")
        axes[0].set_xticklabels(["Retained", "Churned"])
    else:
        sns.histplot(data=df, x="monthly_charges", kde=True, ax=axes[0], color="steelblue")
        axes[0].set_title("Monthly Charges Distribution")

    sns.countplot(data=df, x="contract_type", ax=axes[1], palette="viridis")
    axes[1].set_title("Customers by Contract Type")
    axes[1].tick_params(axis="x", rotation=15)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    # Row 2: Tenure vs charges + payment method
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    if "churn" in df.columns:
        sns.boxplot(data=df, x="churn", y="monthly_charges", ax=axes[0], palette="Set2")
        axes[0].set_title("Monthly Charges by Churn Status")
        axes[0].set_xticklabels(["Retained", "Churned"])
    else:
        sns.scatterplot(data=df, x="tenure", y="monthly_charges", alpha=0.4, ax=axes[0])
        axes[0].set_title("Tenure vs Monthly Charges")

    if "churn" in df.columns:
        churn_by_payment = df.groupby("payment_method")["churn"].mean().reset_index()
        sns.barplot(data=churn_by_payment, x="payment_method", y="churn", ax=axes[1], palette="rocket")
        axes[1].set_title("Churn Rate by Payment Method")
        axes[1].set_ylabel("Churn Rate")
    else:
        sns.countplot(data=df, x="payment_method", ax=axes[1], palette="rocket")
        axes[1].set_title("Customers by Payment Method")

    axes[1].tick_params(axis="x", rotation=20)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    # Correlation heatmap (numeric columns only)
    st.subheader("Feature Correlations")
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if len(numeric_cols) >= 2:
        fig, ax = plt.subplots(figsize=(8, 5))
        corr = df[numeric_cols].corr()
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
        st.pyplot(fig)
        plt.close()


def render_predictions(df: pd.DataFrame, model):
    """Generate and display churn predictions."""
    st.subheader("Churn Predictions")

    feature_df = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    predictions = model.predict(feature_df)
    probabilities = model.predict_proba(feature_df)[:, 1]

    result_df = df[["customer_id"] + NUMERIC_FEATURES + CATEGORICAL_FEATURES].copy()
    result_df["churn_prediction"] = predictions
    result_df["churn_probability"] = probabilities.round(4)
    result_df["risk_level"] = pd.cut(
        probabilities,
        bins=[0, 0.3, 0.6, 1.0],
        labels=["Low", "Medium", "High"],
    )

    # Summary metrics
    high_risk = (result_df["risk_level"] == "High").sum()
    med_risk = (result_df["risk_level"] == "Medium").sum()
    low_risk = (result_df["risk_level"] == "Low").sum()

    c1, c2, c3 = st.columns(3)
    c1.metric("High Risk", high_risk)
    c2.metric("Medium Risk", med_risk)
    c3.metric("Low Risk", low_risk)

    # Filter controls
    risk_filter = st.multiselect(
        "Filter by risk level",
        options=["Low", "Medium", "High"],
        default=["Low", "Medium", "High"],
    )
    filtered = result_df[result_df["risk_level"].isin(risk_filter)]
    st.dataframe(filtered.sort_values("churn_probability", ascending=False), use_container_width=True)

    # Download predictions
    csv_bytes = filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Predictions CSV",
        data=csv_bytes,
        file_name="churn_predictions.csv",
        mime="text/csv",
    )


def render_single_prediction(model):
    st.markdown("---")
    st.header("Predict Churn for 1 New Customer")

    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.number_input("Age", 18, 80, 35)
        tenure = st.number_input("Tenure in Months", 0, 72, 12)
    with col2:
        monthly_charges = st.number_input("Monthly Charges", 10.0, 500.0, 70.0)
        total_charges = st.number_input("Total Charges", 0.0, 10000.0, 840.0)
    with col3:
        contract_type = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
        payment_method = st.selectbox("Payment Method", ["Electronic check", "Mailed check", "Bank transfer", "Credit card"])

    if st.button("Predict Churn", type="primary"):
        import pandas as pd
        new_data = pd.DataFrame([{
            "age": age, 
            "tenure": tenure, 
            "monthly_charges": monthly_charges,
            "total_charges": total_charges, 
            "contract_type": contract_type, 
            "payment_method": payment_method
        }])
        
        prediction = model.predict(new_data)[0]
        prob = model.predict_proba(new_data)[0][1]
        
        if prediction == 1:
            st.error(f"⚠️ High Risk to Churn! Probability: {prob:.2%}")
        else:
            st.success(f"✅ Low Risk. Will Stay. Probability: {1-prob:.2%}")
def main():
    # HEADER WITH LOGO
    col1, col2 = st.columns([1, 6])
    with col1:
        st.image("https://i.imgur.com/8Km9tLL.png", width=80)  # temp logo
    with col2:
        st.title("Customer Churn Prediction Dashboard")
        st.markdown("*Powered by Machine Learning | Data-Driven Retention Insights*")

    st.markdown("Upload a customer CSV to explore the data and predict churn using the trained ML model.")
    st.markdown("---")
    model = load_model()

    uploaded_file = st.file_uploader("Upload customer CSV", type=["csv"])

    # Default to bundled sample data if no upload
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success(f"Loaded {len(df):,} rows from uploaded file.")
    else:
        sample_path = os.path.join(PROJECT_ROOT, "data", "customers.csv")
        if os.path.exists(sample_path):
            df = pd.read_csv(sample_path)
            st.info(f"Using sample dataset ({len(df):,} rows). Upload a CSV to use your own data.")
        else:
            st.warning("No data available. Upload a CSV or run `python src/generate_data.py`.")
            st.stop()

    if not validate_columns(df):
        st.stop()

    tab_eda, tab_predict = st.tabs(["EDA", "Predictions"])

    with tab_eda:
        render_eda(df)

    with tab_predict:
        render_predictions(df, model)
        render_single_prediction(model)


if __name__ == "__main__":
    main()
