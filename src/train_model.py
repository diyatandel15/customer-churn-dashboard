"""
Train churn prediction models and save the best one.
Run: python src/train_model.py
"""

import os
import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from xgboost import XGBClassifier

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "customers.csv")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "churn_model.joblib")

NUMERIC_FEATURES = ["age", "tenure", "monthly_charges", "total_charges"]
CATEGORICAL_FEATURES = ["contract_type", "payment_method"]
TARGET = "churn"


def build_preprocessor():
    return ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), NUMERIC_FEATURES),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CATEGORICAL_FEATURES),
        ]
    )


def build_logistic_regression():
    return Pipeline([
        ("preprocessor", build_preprocessor()),
        ("classifier", LogisticRegression(max_iter=1000, random_state=42)),
    ])


def build_xgboost():
    return Pipeline([
        ("preprocessor", build_preprocessor()),
        ("classifier", XGBClassifier(
            n_estimators=100,
            max_depth=4,
            learning_rate=0.1,
            random_state=42,
            eval_metric="logloss",
        )),
    ])


def main():
    df = pd.read_csv(DATA_PATH)
    X = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    models = {
        "LogisticRegression": build_logistic_regression(),
        "XGBoost": build_xgboost(),
    }

    best_name = None
    best_model = None
    best_acc = 0.0

    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        print(f"\n{'='*50}")
        print(f"Model: {name}")
        print(f"Accuracy: {acc:.4f}")
        print(f"Confusion Matrix:\n{confusion_matrix(y_test, y_pred)}")
        print(classification_report(y_test, y_pred, target_names=["Retained", "Churned"]))

        if acc > best_acc:
            best_acc = acc
            best_name = name
            best_model = model

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(best_model, MODEL_PATH)
    print(f"\nBest model: {best_name} (accuracy={best_acc:.4f})")
    print(f"Saved to: {MODEL_PATH}")


if __name__ == "__main__":
    main()
