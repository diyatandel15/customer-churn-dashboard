"""
Generate synthetic customer churn dataset (10,000 rows).
Run: python src/generate_data.py
"""

import os
import numpy as np
import pandas as pd

np.random.seed(42)

N_ROWS = 10_000
CONTRACT_TYPES = ["Month-to-month", "One year", "Two year"]
PAYMENT_METHODS = ["Electronic check", "Mailed check", "Bank transfer", "Credit card"]

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "customers.csv")


def generate_churn_probability(age, tenure, monthly_charges, contract_type, payment_method):
    """Compute churn probability based on feature values."""
    prob = 0.15

    # Shorter tenure increases churn
    prob += np.where(tenure < 12, 0.25, 0.0)
    prob += np.where((tenure >= 12) & (tenure < 24), 0.10, 0.0)

    # Month-to-month contracts churn more
    prob += np.where(contract_type == "Month-to-month", 0.30, 0.0)
    prob += np.where(contract_type == "One year", -0.10, 0.0)
    prob += np.where(contract_type == "Two year", -0.20, 0.0)

    # Electronic check correlates with higher churn
    prob += np.where(payment_method == "Electronic check", 0.15, 0.0)

    # Higher monthly charges increase churn slightly
    prob += (monthly_charges - 50) / 200

    # Younger customers slightly more likely to churn
    prob += np.where(age < 30, 0.05, 0.0)

    return np.clip(prob, 0.05, 0.95)


def main():
    customer_ids = [f"CUST_{i:05d}" for i in range(1, N_ROWS + 1)]
    ages = np.random.randint(18, 75, size=N_ROWS)
    tenures = np.random.exponential(scale=24, size=N_ROWS).astype(int)
    tenures = np.clip(tenures, 0, 72)

    monthly_charges = np.round(np.random.uniform(20, 120, size=N_ROWS), 2)
    contract_types = np.random.choice(CONTRACT_TYPES, size=N_ROWS, p=[0.45, 0.35, 0.20])
    payment_methods = np.random.choice(PAYMENT_METHODS, size=N_ROWS, p=[0.30, 0.15, 0.30, 0.25])

    total_charges = np.round(monthly_charges * tenures + np.random.normal(0, 50, N_ROWS), 2)
    total_charges = np.maximum(total_charges, 0)

    churn_probs = generate_churn_probability(
        ages, tenures, monthly_charges, contract_types, payment_methods
    )
    churn = (np.random.random(N_ROWS) < churn_probs).astype(int)

    df = pd.DataFrame({
        "customer_id": customer_ids,
        "age": ages,
        "tenure": tenures,
        "monthly_charges": monthly_charges,
        "total_charges": total_charges,
        "contract_type": contract_types,
        "payment_method": payment_methods,
        "churn": churn,
    })

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Generated {len(df):,} rows -> {OUTPUT_PATH}")
    print(f"Churn rate: {df['churn'].mean():.2%}")


if __name__ == "__main__":
    main()
