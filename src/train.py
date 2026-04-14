print("🔥 TRAIN FILE STARTED")

import pandas as pd
import joblib
import os
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from src.preprocessing import preprocess_data   


def train_threat_model(train_path):

    print("📂 Step 1: Loading dataset...")
    train_df = pd.read_csv(train_path)
    print("✅ Dataset loaded successfully")

    print("⚙ Step 2: Preprocessing data...")
    X, y, encoders, scaler = preprocess_data(train_df)
    print("✅ Preprocessing done")

    print("✂ Step 3: Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print("✅ Train-test split done")

    print("🤖 Step 4: Initializing model...")
    model = XGBClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=5,
        eval_metric='logloss'
    )

    print("🚀 Step 5: Training model...")
    model.fit(X_train, y_train)
    print("✅ Model training completed")

    print("🔮 Step 6: Making predictions...")
    y_pred = model.predict(X_test)

    print("\n📊 Step 7: Evaluation Report:\n")
    print(classification_report(y_test, y_pred))

    print("\n📉 Step 8: Confusion Matrix:\n")
    print(confusion_matrix(y_test, y_pred))

    print("💾 Step 9: Saving model files...")
    os.makedirs("models", exist_ok=True)

    joblib.dump(model, 'models/threat_model.pkl')
    joblib.dump(encoders, 'models/encoders.pkl')
    joblib.dump(scaler, 'models/scaler.pkl')

    print("✅ Step 10: All files saved successfully!")


if __name__ == "__main__":
    print("▶ Running main function...")
    train_threat_model('data/UNSW_NB15_training-set.csv')