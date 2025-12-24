import pandas as pd
import xgboost as xgb
import lightgbm as lgb
from sklearn.ensemble import RandomForestClassifier, StackingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
import joblib
import os
import numpy as np

def train_ensemble_model():
    """Trains and tunes a StackingClassifier on advanced feature-engineered data."""
    print("Starting ENSEMBLE model training and hyperparameter tuning...")

    try:
        df = pd.read_csv('data/processed/featured_basketball_data_advanced.csv')
        print(f"Loaded {len(df)} games from advanced processed data.")
    except FileNotFoundError:
        print("Error: 'data/processed/featured_basketball_data_advanced.csv' not found.")
        print("Please run the advanced feature engineering script first.")
        return

    features = [
        'Home_Avg_MOV', 'Home_Avg_Pts_For', 'Home_Avg_Pts_Against', 'Home_Avg_OU_Hit_Rate',
        'Away_Avg_MOV', 'Away_Avg_Pts_For', 'Away_Avg_Pts_Against', 'Away_Avg_OU_Hit_Rate',
        'Avg_MOV_Diff', 'Avg_Pts_For_Diff', 'Avg_Pts_Against_Diff', 'Avg_OU_Hit_Rate_Diff'
    ]
    target = 'OU_Result'

    X = df[features]
    y = df[target]

    print("Features used for training:")
    print(X.columns.tolist())
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"Data split into training ({len(X_train)} samples) and testing ({len(X_test)} samples).")

    print("--- Training and Tuning XGBoost Base Model ---")
    xgb_param_grid = {
        'n_estimators': [100, 200, 300],
        'learning_rate': [0.05, 0.1, 0.2],
        'max_depth': [3, 5],
        'subsample': [0.7, 0.9],
        'colsample_bytree': [0.7, 0.9],
        'gamma': [0, 0.1]
    }
    xgb_base = xgb.XGBClassifier(objective='binary:logistic', use_label_encoder=False, eval_metric='logloss', random_state=42)
    xgb_search = RandomizedSearchCV(xgb_base, xgb_param_grid, n_iter=10, scoring='roc_auc', cv=3, verbose=0, random_state=42, n_jobs=-1)
    xgb_search.fit(X_train, y_train)
    best_xgb = xgb_search.best_estimator_
    print(f"Best XGBoost Params: {xgb_search.best_params_}")

    print("--- Training and Tuning LightGBM Base Model ---")
    lgbm_param_grid = {
        'n_estimators': [100, 200, 300],
        'learning_rate': [0.05, 0.1, 0.2],
        'max_depth': [3, 5, 7],
        'subsample': [0.7, 0.9],
        'colsample_bytree': [0.7, 0.9],
    }
    lgbm_base = lgb.LGBMClassifier(objective='binary', random_state=42)
    lgbm_search = RandomizedSearchCV(lgbm_base, lgbm_param_grid, n_iter=10, scoring='roc_auc', cv=3, verbose=0, random_state=42, n_jobs=-1)
    lgbm_search.fit(X_train, y_train)
    best_lgbm = lgbm_search.best_estimator_
    print(f"Best LightGBM Params: {lgbm_search.best_params_}")

    print("--- Training and Tuning RandomForest Base Model ---")
    rf_param_grid = {
        'n_estimators': [100, 200, 300],
        'max_depth': [5, 10, 15],
        'min_samples_leaf': [1, 5, 10],
        'min_samples_split': [2, 5, 10]
    }
    rf_base = RandomForestClassifier(random_state=42)
    rf_search = RandomizedSearchCV(rf_base, rf_param_grid, n_iter=10, scoring='roc_auc', cv=3, verbose=0, random_state=42, n_jobs=-1)
    rf_search.fit(X_train, y_train)
    best_rf = rf_search.best_estimator_
    print(f"Best RandomForest Params: {rf_search.best_params_}")

    print("--- Building Stacking Ensemble Model ---")
    estimators = [
        ('xgb', best_xgb),
        ('lgbm', best_lgbm),
        ('rf', best_rf)
    ]
    
    stk_model = StackingClassifier(
        estimators=estimators, 
        final_estimator=LogisticRegression(random_state=42, solver='liblinear'),
        cv=3,
        n_jobs=-1,
        verbose=1
    )

    print("Fitting Stacking Ensemble Model...")
    stk_model.fit(X_train, y_train)

    print("Evaluating Stacking Ensemble Model performance...")
    y_pred = stk_model.predict(X_test)
    y_pred_proba = stk_model.predict_proba(X_test)[:, 1]

    accuracy = accuracy_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_pred_proba)
    
    print(f"Ensemble Model Accuracy: {accuracy:.4f}")
    print(f"Ensemble Model AUC-ROC Score: {roc_auc:.4f}")
    
    print("Ensemble Model Classification Report:")
    print(classification_report(y_test, y_pred, target_names=['Under', 'Over']))

    os.makedirs('models', exist_ok=True)
    model_path = 'models/xgb_lgbm_rf_stacking_model.joblib'
    joblib.dump(stk_model, model_path)
    
    print(f"Ensemble model saved successfully to '{model_path}'")

if __name__ == "__main__":
    train_ensemble_model()