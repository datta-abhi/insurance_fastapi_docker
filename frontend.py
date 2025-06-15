import streamlit as st
import requests

API_URL = "http://localhost:8000/predict"

# create title and description
st.title("Insurance premium Category Predictor")
st.markdown("Enter the details below")

# input fields
age = st.number_input("Age", min_value=10, max_value=120, value=30)
weight = st.number_input("Weight (kg)", min_value=1.0, max_value=300.0, value=70.0)
height = st.number_input("Height (m)", min_value=0.5, max_value=2.5, value=1.5)
income_lpa = st.number_input("Income (LPA)", min_value=0.1, value=10.0)
smoker = st.selectbox("Are you a smoker?", options=[True,False])
city = st.text_input("City", value="Mumbai")
occupation = st.selectbox("Occupation", 
                          ['retired', 'freelancer', 'student', 'government_job', 'business_owner', 'unemployed', 'private_job'])

if st.button("Predict Premium Category"):
    # Prepare the data for the API request
    data = {
        "age": age,
        "weight": weight,
        "height": height,
        "income_lpa": income_lpa,
        "smoker": smoker,
        "city": city,
        "occupation": occupation
    }
    
    try:
        # Make the API request
        response = requests.post(API_URL, json=data)
        result = response.json()

        if response.status_code == 200:
            prediction = result['premium_category']
            st.success(f"Predicted Premium Category: **{prediction}**")
            
        else:
            st.error(f"API error: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")
        st.error("Please ensure the backend service is running.")        