from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import os
import numpy as np

app = FastAPI()

# Allow CORS for your frontend origin(s)
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3000/frontend/index.html",  # add your actual frontend origin here
    "http://127.0.0.1",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load your trained model (ensure the model file path is correct)
model = joblib.load(os.path.join(os.path.dirname(__file__), 'models', 'loan_risk_model.pkl'))

# Define input model to match all required features
class LoanApplication(BaseModel):
    Gender: str
    Married: str
    Dependents: str
    Education: str
    Self_Employed: str
    ApplicantIncome: float
    CoapplicantIncome: float
    LoanAmount: float
    Loan_Amount_Term: float
    Credit_History: float
    Property_Area: str

# Dummy encoding maps (example)
gender_map = {"Male": 1, "Female": 0}
married_map = {"Yes": 1, "No": 0}
education_map = {"Graduate": 1, "Not Graduate": 0}
self_employed_map = {"Yes": 1, "No": 0}
property_area_map = {"Urban": 2, "Semiurban": 1, "Rural": 0}
# Dependents map: "3+" as 3 for numeric
dependents_map = {"0": 0, "1": 1, "2": 2, "3+": 3}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Loan Risk Prediction API"}

@app.post("/predict/")
def predict_loan_risk(loan: LoanApplication):
    # Convert categorical values to numeric as model expects
    try:
        gender = gender_map[loan.Gender]
        married = married_map[loan.Married]
        education = education_map[loan.Education]
        self_employed = self_employed_map[loan.Self_Employed]
        property_area = property_area_map[loan.Property_Area]
        dependents = dependents_map[loan.Dependents]
    except KeyError as e:
        return {"error": f"Invalid category for {str(e)}"}

    # Prepare feature vector in correct order your model expects
    features = np.array([
        gender,
        married,
        dependents,
        education,
        self_employed,
        loan.ApplicantIncome,
        loan.CoapplicantIncome,
        loan.LoanAmount,
        loan.Loan_Amount_Term,
        loan.Credit_History,
        property_area
    ]).reshape(1, -1)

    # Predict
    prediction = model.predict(features)
    risk = "High Risk" if prediction[0] == 1 else "Low Risk"

    return {"prediction": risk}
