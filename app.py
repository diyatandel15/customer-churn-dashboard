import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt


# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="Customer Churn Prediction",
    page_icon="📊",
    layout="wide"
)


# =========================================================
# LOAD MODEL AND DATA
# =========================================================

bundle = joblib.load("churn_model.pkl")

model = bundle["model"]
scaler = bundle["scaler"]
model_columns = bundle["model_columns"]
numerical_cols = bundle["numerical_cols"]

df = pd.read_csv("churn_dataset.csv")


# =========================================================
# HEADER
# =========================================================

st.title("📊 Customer Churn Prediction")

st.write(
    "Explore customer churn patterns and predict the likelihood "
    "of customer churn using machine learning."
)


# =========================================================
# TWO MAIN SECTIONS
# =========================================================

eda_tab, prediction_tab = st.tabs(
    ["📈 EDA", "🔮 Predictions"]
)


# =========================================================
# EDA TAB
# =========================================================

with eda_tab:

    st.header("Exploratory Data Analysis")

    # -----------------------------------------------------
    # KPI METRICS
    # -----------------------------------------------------

    total_customers = len(df)

    churned_customers = (
        df["Churn"] == "Yes"
    ).sum()

    retained_customers = (
        df["Churn"] == "No"
    ).sum()

    churn_rate = (
        churned_customers / total_customers
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Customers",
            f"{total_customers:,}"
        )

    with col2:
        st.metric(
            "Churn Rate",
            f"{churn_rate:.1%}"
        )

    with col3:
        st.metric(
            "Churned",
            f"{churned_customers:,}"
        )

    with col4:
        st.metric(
            "Retained",
            f"{retained_customers:,}"
        )

    st.divider()


    # =====================================================
    # FIRST ROW OF CHARTS
    # =====================================================

    chart_col1, chart_col2 = st.columns(2)


    # -----------------------------------------------------
    # CHART 1 - CHURN DISTRIBUTION
    # -----------------------------------------------------

    with chart_col1:

        churn_rates = [
            retained_customers / total_customers * 100,
            churned_customers / total_customers * 100
        ]

        churn_labels = [
            "Retained",
            "Churned"
        ]

        fig1, ax1 = plt.subplots(figsize=(7, 4))

        bars1 = ax1.bar(
            churn_labels,
            churn_rates,
            color="#2878B5",
            width=0.6
        )

        ax1.set_title(
            "Churn Distribution",
            fontsize=14,
            pad=12
        )

        ax1.set_ylabel("Percentage (%)")

        ax1.spines["top"].set_visible(False)
        ax1.spines["right"].set_visible(False)

        ax1.bar_label(
            bars1,
            labels=[
                f"{value:.1f}%"
                for value in churn_rates
            ],
            padding=3,
            fontsize=10
        )

        ax1.set_ylim(0, 100)

        fig1.tight_layout()

        st.pyplot(
            fig1,
            use_container_width=True
        )

        plt.close(fig1)


    # -----------------------------------------------------
    # CHART 2 - CHURN RATE BY CONTRACT TYPE
    # -----------------------------------------------------

    with chart_col2:

        contract_churn = (
            df.groupby("Contract")["Churn"]
            .apply(
                lambda x: (x == "Yes").mean() * 100
            )
        )

        fig2, ax2 = plt.subplots(figsize=(7, 4))

        bars2 = ax2.bar(
            contract_churn.index,
            contract_churn.values,
            color="#2878B5",
            width=0.6
        )

        ax2.set_title(
            "Churn Rate by Contract Type",
            fontsize=14,
            pad=12
        )

        ax2.set_ylabel("Churn Rate (%)")

        ax2.spines["top"].set_visible(False)
        ax2.spines["right"].set_visible(False)

        ax2.bar_label(
            bars2,
            labels=[
                f"{value:.1f}%"
                for value in contract_churn.values
            ],
            padding=3,
            fontsize=10
        )

        ax2.set_ylim(
            0,
            max(contract_churn.values) * 1.15
        )

        plt.xticks(
            rotation=0
        )

        fig2.tight_layout()

        st.pyplot(
            fig2,
            use_container_width=True
        )

        plt.close(fig2)


    # =====================================================
    # SECOND ROW OF CHARTS
    # =====================================================

    chart_col3, chart_col4 = st.columns(2)


    # -----------------------------------------------------
    # CHART 3 - CHURN RATE BY TENURE
    # -----------------------------------------------------

    with chart_col3:

        tenure_data = df.copy()

        tenure_data["Tenure Group"] = pd.cut(
            tenure_data["tenure"],
            bins=[
                -1,
                12,
                24,
                36,
                48,
                60,
                72
            ],
            labels=[
                "0-12 months",
                "13-24 months",
                "25-36 months",
                "37-48 months",
                "49-60 months",
                "61-72 months"
            ]
        )

        tenure_churn = (
            tenure_data
            .groupby(
                "Tenure Group",
                observed=False
            )["Churn"]
            .apply(
                lambda x: (x == "Yes").mean() * 100
            )
        )

        fig3, ax3 = plt.subplots(figsize=(7, 4))

        bars3 = ax3.bar(
            tenure_churn.index.astype(str),
            tenure_churn.values,
            color="#2878B5",
            width=0.65
        )

        ax3.set_title(
            "Churn Rate by Tenure",
            fontsize=14,
            pad=12
        )

        ax3.set_ylabel("Churn Rate (%)")

        ax3.spines["top"].set_visible(False)
        ax3.spines["right"].set_visible(False)

        ax3.bar_label(
            bars3,
            labels=[
                f"{value:.1f}%"
                for value in tenure_churn.values
            ],
            padding=3,
            fontsize=9
        )

        ax3.set_ylim(
            0,
            max(tenure_churn.values) * 1.15
        )

        plt.xticks(
            rotation=0,
            fontsize=9
        )

        fig3.tight_layout()

        st.pyplot(
            fig3,
            use_container_width=True
        )

        plt.close(fig3)


    # -----------------------------------------------------
    # CHART 4 - CHURN RATE BY MONTHLY CHARGES
    # -----------------------------------------------------

    with chart_col4:

        charges_data = df.copy()

        charges_data["Charge Group"] = pd.cut(
            charges_data["MonthlyCharges"],
            bins=[
                0,
                40,
                60,
                80,
                100,
                120
            ],
            labels=[
                "Under $40",
                "$40-$60",
                "$60-$80",
                "$80-$100",
                "$100+"
            ]
        )

        charges_churn = (
            charges_data
            .groupby(
                "Charge Group",
                observed=False
            )["Churn"]
            .apply(
                lambda x: (x == "Yes").mean() * 100
            )
        )

        fig4, ax4 = plt.subplots(figsize=(7, 4))

        bars4 = ax4.bar(
            charges_churn.index.astype(str),
            charges_churn.values,
            color="#2878B5",
            width=0.65
        )

        ax4.set_title(
            "Churn Rate by Monthly Charges",
            fontsize=14,
            pad=12
        )

        ax4.set_ylabel("Churn Rate (%)")

        ax4.spines["top"].set_visible(False)
        ax4.spines["right"].set_visible(False)

        ax4.bar_label(
            bars4,
            labels=[
                f"{value:.1f}%"
                for value in charges_churn.values
            ],
            padding=3,
            fontsize=9
        )

        ax4.set_ylim(
            0,
            max(charges_churn.values) * 1.15
        )

        plt.xticks(
            rotation=0,
            fontsize=9
        )

        fig4.tight_layout()

        st.pyplot(
            fig4,
            use_container_width=True
        )

        plt.close(fig4)


# =========================================================
# PREDICTION TAB
# =========================================================

with prediction_tab:

    st.header("Customer Churn Prediction")

    st.write(
        "Enter customer details below to predict the likelihood "
        "of customer churn."
    )


    # =====================================================
    # CUSTOMER CHARGES AND TENURE
    # =====================================================

    st.subheader("💰 Customer Charges and Tenure")

    col1, col2 = st.columns(2)

    with col1:

        tenure = st.number_input(
            "Tenure (months)",
            min_value=0,
            max_value=72,
            value=12,
            step=1
        )

    with col2:

        monthly_charges = st.number_input(
            "Monthly Charges",
            min_value=18.25,
            max_value=118.75,
            value=70.0,
            step=1.0
        )

    total_charges = st.number_input(
        "Total Charges",
        min_value=0.0,
        max_value=8684.80,
        value=500.0,
        step=1.0
    )


    # =====================================================
    # CUSTOMER PROFILE
    # =====================================================

    st.subheader("👤 Customer Profile")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        gender = st.selectbox(
            "Gender",
            ["Female", "Male"]
        )

    with col2:

        senior_citizen = st.selectbox(
            "Senior Citizen",
            [0, 1]
        )

    with col3:

        partner = st.selectbox(
            "Partner",
            ["No", "Yes"]
        )

    with col4:

        dependents = st.selectbox(
            "Dependents",
            ["No", "Yes"]
        )


    # =====================================================
    # SERVICES
    # =====================================================

    st.subheader("🔧 Services")

    col1, col2, col3 = st.columns(3)

    with col1:

        phone_service = st.selectbox(
            "Phone Service",
            ["No", "Yes"]
        )

        multiple_lines = st.selectbox(
            "Multiple Lines",
            [
                "No",
                "Yes",
                "No phone service"
            ]
        )

        internet_service = st.selectbox(
            "Internet Service",
            [
                "DSL",
                "Fiber optic",
                "No"
            ]
        )

    with col2:

        online_security = st.selectbox(
            "Online Security",
            [
                "No",
                "Yes",
                "No internet service"
            ]
        )

        online_backup = st.selectbox(
            "Online Backup",
            [
                "No",
                "Yes",
                "No internet service"
            ]
        )

        device_protection = st.selectbox(
            "Device Protection",
            [
                "No",
                "Yes",
                "No internet service"
            ]
        )

    with col3:

        tech_support = st.selectbox(
            "Tech Support",
            [
                "No",
                "Yes",
                "No internet service"
            ]
        )

        streaming_tv = st.selectbox(
            "Streaming TV",
            [
                "No",
                "Yes",
                "No internet service"
            ]
        )

        streaming_movies = st.selectbox(
            "Streaming Movies",
            [
                "No",
                "Yes",
                "No internet service"
            ]
        )


    # =====================================================
    # CONTRACT AND BILLING
    # =====================================================

    st.subheader("💳 Contract and Billing")

    col1, col2 = st.columns(2)

    with col1:

        contract = st.selectbox(
            "Contract",
            [
                "Month-to-month",
                "One year",
                "Two year"
            ]
        )

        paperless_billing = st.selectbox(
            "Paperless Billing",
            ["No", "Yes"]
        )

    with col2:

        payment_method = st.selectbox(
            "Payment Method",
            [
                "Electronic check",
                "Mailed check",
                "Bank transfer (automatic)",
                "Credit card (automatic)"
            ]
        )


    # =====================================================
    # PREDICT BUTTON
    # =====================================================

    st.divider()

    predict_button = st.button(
        "🔍 Predict Churn",
        use_container_width=True
    )


    # =====================================================
    # PREDICTION
    # =====================================================

    if predict_button:

        input_data = pd.DataFrame({

            "gender": [gender],

            "SeniorCitizen": [
                senior_citizen
            ],

            "Partner": [
                partner
            ],

            "Dependents": [
                dependents
            ],

            "tenure": [
                tenure
            ],

            "PhoneService": [
                phone_service
            ],

            "MultipleLines": [
                multiple_lines
            ],

            "InternetService": [
                internet_service
            ],

            "OnlineSecurity": [
                online_security
            ],

            "OnlineBackup": [
                online_backup
            ],

            "DeviceProtection": [
                device_protection
            ],

            "TechSupport": [
                tech_support
            ],

            "StreamingTV": [
                streaming_tv
            ],

            "StreamingMovies": [
                streaming_movies
            ],

            "Contract": [
                contract
            ],

            "PaperlessBilling": [
                paperless_billing
            ],

            "PaymentMethod": [
                payment_method
            ],

            "MonthlyCharges": [
                monthly_charges
            ],

            "TotalCharges": [
                total_charges
            ]
        })


        # -------------------------------------------------
        # CATEGORICAL COLUMNS
        # -------------------------------------------------

        categorical_input_cols = [

            "gender",
            "Partner",
            "Dependents",
            "PhoneService",
            "MultipleLines",
            "InternetService",
            "OnlineSecurity",
            "OnlineBackup",
            "DeviceProtection",
            "TechSupport",
            "StreamingTV",
            "StreamingMovies",
            "Contract",
            "PaperlessBilling",
            "PaymentMethod"

        ]


        # -------------------------------------------------
        # ONE-HOT ENCODING
        # -------------------------------------------------

        input_data = pd.get_dummies(
            input_data,
            columns=categorical_input_cols,
            drop_first=True
        )


        # -------------------------------------------------
        # MATCH TRAINING COLUMNS
        # -------------------------------------------------

        input_data = input_data.reindex(
            columns=model_columns,
            fill_value=0
        )


        # -------------------------------------------------
        # SCALE NUMERICAL FEATURES
        # -------------------------------------------------

        input_data[numerical_cols] = (
            scaler.transform(
                input_data[numerical_cols]
            )
        )


        # -------------------------------------------------
        # MODEL PREDICTION
        # -------------------------------------------------

        prediction = model.predict(
            input_data
        )[0]

        probability = model.predict_proba(
            input_data
        )[0][1]


        # =================================================
        # RESULT
        # =================================================

        st.subheader("📊 Prediction Result")

        result_col1, result_col2 = st.columns(2)

        with result_col1:

            if prediction == 1:

                st.error(
                    "⚠️ Customer is likely to churn."
                )

            else:

                st.success(
                    "✅ Customer is unlikely to churn."
                )

        with result_col2:

            st.metric(
                "Churn Probability",
                f"{probability:.2%}"
            )


        # =================================================
        # RISK LEVEL
        # =================================================

        if probability >= 0.70:

            st.error(
                "🔴 High Risk — The customer has a high "
                "probability of churn."
            )

        elif probability >= 0.40:

            st.warning(
                "🟡 Medium Risk — The customer has a moderate "
                "probability of churn."
            )

        else:

            st.success(
                "🟢 Low Risk — The customer has a relatively "
                "low probability of churn."
            )


    # =====================================================
    # DISCLAIMER
    # =====================================================

    st.divider()

    st.caption(
        "Prediction is based on the trained machine-learning "
        "model and is not a guarantee of actual customer behavior."
    )