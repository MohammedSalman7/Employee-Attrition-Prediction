# Import libraries
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# Load dataset
df = pd.read_csv(
    "dataset/WA_Fn-UseC_-HR-Employee-Attrition.csv"
)

# Convert target variable
df["Attrition"] = df["Attrition"].map(
    {"Yes": 1, "No": 0}
)

# Label Encoding
le = LabelEncoder()

for col in df.select_dtypes(include="object").columns:
    if col != "Attrition":
        df[col] = le.fit_transform(df[col])

# Features and Target
X = df.drop("Attrition", axis=1)
y = df["Attrition"]

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Scaling
scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train Model
model = LogisticRegression(
    max_iter=1000
)

model.fit(X_train, y_train)

# Prediction
y_pred = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(
    y_test,
    y_pred
)

print("Accuracy:", accuracy)

print(
    classification_report(
        y_test,
        y_pred
    )
)

# Save Model
joblib.dump(
    model,
    "model/attrition_model.pkl"
)

joblib.dump(
    scaler,
    "model/scaler.pkl"
)

print("Model Saved Successfully!")