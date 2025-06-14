# necessary imports
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Literal,Annotated
import pickle
import pandas as pd

# import the model
model_path = './artifacts/model.pkl'
with open(model_path, 'rb') as f:
    model = pickle.load(f)
    
# create the FastAPI app
app = FastAPI()

# Define city tiers
tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = ["Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
                "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Amritsar", "Varanasi",
                "Agra", "Dehradun", "Mysore", "Guwahati", "Thiruvananthapuram", 
                "Allahabad", "Aurangabad", "Vijayawada", "Tiruchirappalli", "Gwalior",  "Warangal", "Noida"]

# pydantic model to validate input data
class UserInput(BaseModel):
    age: Annotated[int, Field(..., ge=0, lt=120, description="Age of the person")]
    weight: Annotated[float, Field(..., ge=0, lt=300, description="weight of the person")]
    height: Annotated[float, Field(..., ge=0, lt=2.5, description="height of the person")]
    income_lpa: Annotated[float, Field(..., ge=0, description="income in LPA of the person")]
    smoker: Annotated[bool, Field(..., description="If Person is smoker")]
    city: Annotated[str, Field(..., description="City of Residence")]
    occupation: Annotated[Literal['retired', 'freelancer', 'student', 'government_job',
                                'business_owner', 'unemployed', 'private_job'], 
                        Field(..., description="Occupation of the person")]
    
    @computed_field
    @property
    def bmi(self) -> float:
        """Calculate BMI from weight and height."""
        return round(self.weight / (self.height ** 2), 2)
    
    @computed_field
    @property
    def age_group(self) -> str:
        """Determine age group based on age."""
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "senior"
    
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        """Determine lifestyle risk based on smoking and BMI."""
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return "low"
    
    @computed_field
    @property
    def city_tier(self) -> int:
        """Determine city tier based on city name."""
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3  
        
# Create prediction endpoint
@app.post("/predict")
def predict_premium(input_data: UserInput):          

    input_df = pd.DataFrame([{'bmi': input_data.bmi,
                   'age_group': input_data.age_group,
                   'lifestyle_risk': input_data.lifestyle_risk,
                   'city_tier': input_data.city_tier,
                   'income_lpa': input_data.income_lpa,
                   'occupation': input_data.occupation}])

    prediction = model.predict(input_df)[0]
    
    return JSONResponse(status_code=200, content={'premium_category': prediction})