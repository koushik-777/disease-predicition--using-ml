import pickle
import os
import streamlit as st
from streamlit_option_menu import option_menu

# Configure page settings
st.set_page_config(page_title="Disease Prediction", page_icon="🧑‍⚕️", layout="wide", initial_sidebar_state="expanded")

# Get the working directory
working_dir = os.path.dirname(os.path.abspath(__file__))

# Load the saved models
def load_model(path):
    try:
        return pickle.load(open(path, 'rb'))
    except FileNotFoundError:
        st.error(f"Model file not found: {path}")
        return None

# Define model paths using os.path.join to ensure correct path resolution
diabetes_model_path = os.path.join(working_dir, 'models', 'diabetes-prediction.sav')
heart_model_path = os.path.join(working_dir, 'models', 'heart-disease-prediction-model.sav')
parkinson_model_path = os.path.join(working_dir, 'models', 'parkinsons_model.sav')

# Load models
diabetes_model = load_model(diabetes_model_path)
heart_model = load_model(heart_model_path)
parkinson_model = load_model(parkinson_model_path)

# Sidebar menu
with st.sidebar:
    selected = option_menu(
        "Disease Prediction",  
        ["Diabetes", "Heart Disease", "Parkinson's Disease"],  
        icons=['activity', 'heart', 'brain'],  
        menu_icon='hospital-fill',  
        default_index=0  
    )

# Diabetes Prediction Page
def diabetes_prediction_page():
    st.title("Diabetes Prediction")
    
    # Input fields
    col1, col2, col3 = st.columns(3)
    
    with col1:
        pregnancies = st.number_input("Number of Pregnancies", step=1)
        skin_thickness = st.number_input("Skin Thickness", step=0.1)
        diabetes_pedigree_function = st.number_input("Diabetes Pedigree Function",  step=0.01)
    
    with col2:
        glucose = st.number_input("Glucose Level",  step=0.1)
        insulin = st.number_input("Insulin Level",  step=0.1)
        age = st.number_input("Age",  step=1)
    
    with col3:
        blood_pressure = st.number_input("Blood Pressure", step=0.1)
        bmi = st.number_input("BMI",  step=0.1)
    
    # Prediction button
    if st.button("Diabetes Test Result"):
        # Validate inputs
        if all([pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, diabetes_pedigree_function, age]):
            user_input = [[pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, diabetes_pedigree_function, age]]
            diabetes_prediction = diabetes_model.predict(user_input)
            
            if diabetes_prediction[0] == 1:
                st.error("You have Diabetes")
            else:
                st.success("You don't have Diabetes")
        else:
            st.warning("Please fill in all fields")

# Heart Disease Prediction Page
def heart_disease_prediction_page():
    st.title("Heart Disease Prediction")
    
    # Input fields
    col1, col2, col3 = st.columns(3)
    
    with col1:
        age = st.number_input("Age", min_value=0, step=1)
        resting_blood_pressure = st.number_input("Resting Blood Pressure", step=0.1)
        resting_ecg = st.number_input("Resting ECG",  step=1)
        st_depression = st.number_input("ST Depression",  step=0.01)
        major_vessels = st.number_input("Major Vessels",  step=1)
    
    with col2:
        sex = st.selectbox("Sex", [0, 1], format_func=lambda x: "Female" if x == 0 else "Male")
        cholesterol = st.number_input("Cholesterol",  step=0.1)
        max_heart_rate = st.number_input("Max Heart Rate",  step=0.1)
        st_slope = st.number_input("Slope of Peak Exercise ST Segment",  step=0.1)
        thalassemia = st.selectbox("Thalassemia", [0, 1, 2], format_func=lambda x: {0: "Normal", 1: "Fixed Defect", 2: "Reversible Defect"}[x])
    
    with col3:
        chestpain = st.selectbox("Chest Pain Type", [0, 1, 2, 3])
        fasting_blood_sugar = st.selectbox("Fasting Blood Sugar > 120 mg/dl", [0, 1])
        exercise_induced_angina = st.selectbox("Exercise Induced Angina", [0, 1])
        maximum_heart_rate = st.number_input("Maximum Heart Rate", min_value=0.0, step=0.1)
    
    # Prediction button
    if st.button("Heart Disease Test Result"):
        # Validate inputs
        user_input = [age, sex, chestpain, resting_blood_pressure, cholesterol, 
                      fasting_blood_sugar, resting_ecg, max_heart_rate, 
                      exercise_induced_angina, st_depression, st_slope, 
                      maximum_heart_rate, major_vessels, thalassemia]
        
        heart_prediction = heart_model.predict([user_input])
        
        if heart_prediction[0] == 1:
            st.error("You have Heart Disease")
        else:
            st.success("You don't have Heart Disease")

# Parkinson's Disease Prediction Page
def parkinsons_prediction_page():
    st.title("Parkinson's Disease Prediction")
    
    # Input fields organized into columns
    cols = st.columns(3)
    input_fields = [
        "MDVP:Fo(Hz)", "MDVP:Fhi(Hz)", "MDVP:Flo(Hz)", 
        "MDVP:Jitter(%)", "MDVP:Jitter(Abs)", "MDVP:RAP", 
        "MDVP:PPQ", "Jitter:DDP", "MDVP:Shimmer", 
        "MDVP:Shimmer(dB)", "Shimmer:APQ3", "Shimmer:APQ5", 
        "MDVP:APQ", "Shimmer:DDA", "NHR", "HNR", 
        "RPDE", "DFA", "spread1", "spread2", "D2", "PPE"
    ]
    
    inputs = {}
    for i, field in enumerate(input_fields):
        col_index = i % 3
        with cols[col_index]:
            inputs[field] = st.number_input(field,  step=0.01)
    
    # Prediction button
    if st.button("Parkinson's Disease Test Result"):
        user_input = [inputs[field] for field in input_fields]
        
        parkinson_prediction = parkinson_model.predict([user_input])
        
        if parkinson_prediction[0] == 1:
            st.error("You have Parkinson's Disease")
        else:
            st.success("You don't have Parkinson's Disease")

# Main app logic
def main():
    if selected == "Diabetes":
        diabetes_prediction_page()
    elif selected == "Heart Disease":
        heart_disease_prediction_page()
    elif selected == "Parkinson's Disease":
        parkinsons_prediction_page()

if __name__ == "__main__":
    main()
