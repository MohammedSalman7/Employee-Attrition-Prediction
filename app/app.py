from flask import Flask, render_template, request
import pandas as pd
import joblib
import os
from datetime import datetime

app = Flask(__name__)

# ===========================
# Load Model and Scaler
# ===========================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model = joblib.load(
    os.path.join(BASE_DIR, "model", "attrition_model.pkl")
)

scaler = joblib.load(
    os.path.join(BASE_DIR, "model", "scaler.pkl")
)

# ===========================
# Home Page
# ===========================

@app.route('/')
def home():
    return render_template('index.html')


# ===========================
# Prediction Route
# ===========================

@app.route('/predict', methods=['POST'])
def predict():

    try:

        age = int(request.form['age'])
        monthly_income = int(request.form['monthly_income'])
        distance = int(request.form['distance'])
        years_company = int(request.form['years_company'])
        job_satisfaction = int(request.form['job_satisfaction'])
        work_life = int(request.form['work_life'])

        overtime_text = request.form['overtime']
        overtime = 1 if overtime_text == "Yes" else 0

        # Validation
        if age < 18 or age > 60:
            return "Age must be between 18 and 60."

        if job_satisfaction not in [1, 2, 3, 4]:
            return "Job Satisfaction must be between 1 and 4."

        if work_life not in [1, 2, 3, 4]:
            return "Work-Life Balance must be between 1 and 4."

        # Create DataFrame
        data = pd.DataFrame([{
            'Age': age,
            'BusinessTravel': 1,
            'DailyRate': 800,
            'Department': 0,
            'DistanceFromHome': distance,
            'Education': 3,
            'EducationField': 0,
            'EnvironmentSatisfaction': 2,
            'Gender': 0,
            'HourlyRate': 65,
            'JobInvolvement': 3,
            'JobLevel': 2,
            'JobRole': 0,
            'JobSatisfaction': job_satisfaction,
            'MaritalStatus': 1,
            'MonthlyIncome': monthly_income,
            'MonthlyRate': 15000,
            'NumCompaniesWorked': 2,
            'OverTime': overtime,
            'PercentSalaryHike': 15,
            'PerformanceRating': 3,
            'RelationshipSatisfaction': 3,
            'StockOptionLevel': 1,
            'TotalWorkingYears': years_company,
            'TrainingTimesLastYear': 2,
            'WorkLifeBalance': work_life,
            'YearsAtCompany': years_company,
            'YearsInCurrentRole': min(years_company, 3),
            'YearsSinceLastPromotion': min(years_company, 2),
            'YearsWithCurrManager': min(years_company, 3)
        }])

        data_scaled = scaler.transform(data)

        prediction = model.predict(data_scaled)[0]
        probability = model.predict_proba(data_scaled)[0][1]

        if probability >= 0.70:
            risk = "High Risk"
        elif probability >= 0.40:
            risk = "Medium Risk"
        else:
            risk = "Low Risk"

        if prediction == 1:
            result = "Employee is Likely to Leave"
        else:
            result = "Employee is Likely to Stay"

        prediction_time = datetime.now().strftime(
            "%d-%m-%Y %I:%M %p"
        )

        return render_template(
            'result.html',
            result=result,
            probability=round(probability * 100, 2),
            risk=risk,
            prediction_time=prediction_time,
            age=age,
            monthly_income=monthly_income,
            distance=distance,
            years_company=years_company,
            overtime=overtime_text
        )

    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == '__main__':
    app.run(debug=True)