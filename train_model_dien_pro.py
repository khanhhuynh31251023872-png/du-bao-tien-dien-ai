import re
import json
import joblib
import warnings
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.compose import TransformedTargetRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

warnings.filterwarnings("ignore")


def parse_vn_money_to_thousand(x):
    if pd.isna(x):
        return np.nan

    text = str(x).strip()
    text = text.replace("VNĐ", "").replace("vnđ", "").replace("đ", "").replace("Đ", "").replace("?", "")
    text = re.sub(r"[^\d,.\-]", "", text)

    if text == "" or text == "-":
        return np.nan

    if "," in text:
        normalized = text.replace(".", "").replace(",", ".")
    else:
        if text.count(".") > 1:
            normalized = text.replace(".", "")
        elif text.count(".") == 1:
            left, right = text.split(".")
            normalized = left + right if len(right) == 3 else text
        else:
            normalized = text

    try:
        value = float(normalized)
    except ValueError:
        return np.nan

    if value > 10000:
        value = value / 1000

    return value


def load_and_clean_data(path="Book1_clean_no_email.csv"):
    df = pd.read_csv(path)

    required = [
        "People", "AC_Units", "AC_Hours", "Fans",
        "Fan_Hours", "Fridges", "Area", "Cost_Thousand_VND"
    ]

    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"Thiếu cột dữ liệu: {missing}")

    for col in required:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=required)
    df = df[
        (df["People"] >= 1)
        & (df["Area"] > 0)
        & (df["AC_Hours"].between(0, 24))
        & (df["Fan_Hours"].between(0, 24))
        & (df["Cost_Thousand_VND"] > 0)
    ].copy()

    return df


def build_features(df):
    X = df[["People", "AC_Units", "AC_Hours", "Fans", "Fan_Hours", "Fridges", "Area"]].copy()

    X["AC_Load"] = X["AC_Units"] * X["AC_Hours"]
    X["Fan_Load"] = X["Fans"] * X["Fan_Hours"]
    X["Total_Appliances"] = X["AC_Units"] + X["Fans"] + X["Fridges"]
    X["Cooling_Per_Person"] = X["AC_Load"] / (X["People"] + 0.5)
    X["Area_Per_Person"] = X["Area"] / X["People"].replace(0, np.nan)
    X["Device_Density"] = X["Total_Appliances"] / X["Area"].clip(lower=1)

    X = X.replace([np.inf, -np.inf], np.nan).fillna(0)
    return X


def train():
    df = load_and_clean_data()
    X = build_features(df)
    y = df["Cost_Thousand_VND"].astype(float)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )

    candidate_models = {
        "RandomForest": RandomForestRegressor(
            n_estimators=500,
            max_depth=5,
            min_samples_leaf=2,
            random_state=42
        ),
        "ExtraTrees": ExtraTreesRegressor(
            n_estimators=500,
            max_depth=5,
            min_samples_leaf=2,
            random_state=42
        ),
        "GradientBoosting": GradientBoostingRegressor(
            n_estimators=180,
            learning_rate=0.04,
            max_depth=2,
            random_state=42
        ),
        "Ridge_Log": Pipeline([
            ("scaler", StandardScaler()),
            ("ridge", Ridge(alpha=5.0))
        ])
    }

    leaderboard = []
    best_name = None
    best_model = None
    best_mae = float("inf")

    for name, regressor in candidate_models.items():
        model = TransformedTargetRegressor(
            regressor=regressor,
            func=np.log1p,
            inverse_func=np.expm1
        )

        model.fit(X_train, y_train)
        pred = np.maximum(model.predict(X_test), 0)

        mae = mean_absolute_error(y_test, pred)
        rmse = np.sqrt(mean_squared_error(y_test, pred))
        r2 = r2_score(y_test, pred)

        leaderboard.append({
            "model": name,
            "MAE_thousand_VND": round(float(mae), 2),
            "RMSE_thousand_VND": round(float(rmse), 2),
            "R2": round(float(r2), 4)
        })

        if mae < best_mae:
            best_mae = mae
            best_name = name
            best_model = model

    final_model = TransformedTargetRegressor(
        regressor=candidate_models[best_name],
        func=np.log1p,
        inverse_func=np.expm1
    )
    final_model.fit(X, y)

    artifact = {
        "model": final_model,
        "feature_columns": list(X.columns),
        "input_columns": ["People", "AC_Units", "AC_Hours", "Fans", "Fan_Hours", "Fridges", "Area"],
        "metrics": {
            "best_model": best_name,
            "rows_after_cleaning": int(len(df)),
            "target_unit": "nghìn đồng",
            "feature_columns": list(X.columns),
            "leaderboard": leaderboard,
            "note": "Dataset còn nhỏ, chỉ nên xem kết quả là mô hình demo học máy, không phải công cụ dự báo chính xác tuyệt đối."
        }
    }

    joblib.dump(artifact, "model_dien_pro.pkl")

    with open("model_metrics.json", "w", encoding="utf-8") as f:
        json.dump(artifact["metrics"], f, ensure_ascii=False, indent=2)

    print("Đã huấn luyện xong.")
    print("Model tốt nhất:", best_name)
    print(pd.DataFrame(leaderboard))


if __name__ == "__main__":
    train()
