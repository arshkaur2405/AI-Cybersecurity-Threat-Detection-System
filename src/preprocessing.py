import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler


def preprocess_data(df, is_training=True, encoders=None, scaler=None):

    # Drop unnecessary columns
    cols_to_drop = ['id', 'attack_cat']
    df = df.drop(columns=[c for c in cols_to_drop if c in df.columns])

    # Categorical columns
    cat_cols = ['proto', 'service', 'state']

    # =========================
    # ENCODING
    # =========================
    if is_training:
        encoders = {}

        for col in cat_cols:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
            encoders[col] = le

    else:
        # Use trained encoders safely
        for col in cat_cols:
            le = encoders[col]

            # safer mapping
            df[col] = df[col].apply(
                lambda x: le.transform([x])[0] if x in le.classes_ else -1
            )

    # =========================
    # SPLIT FEATURES / LABEL
    # =========================
    X = df.drop(columns=['label']) if 'label' in df.columns else df.copy()
    y = df['label'] if 'label' in df.columns else None

    # =========================
    # SCALING (FIXED)
    # =========================
    if is_training:
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
    else:
        X_scaled = scaler.transform(X)

    return X_scaled, y, encoders, scaler