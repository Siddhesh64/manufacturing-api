import streamlit as st
import pandas as pd
import requests
import io

# Your live API link
API_URL = "https://manufacturing-api-am66.onrender.com/predict"

st.set_page_config(page_title="Factory AI Predictor", layout="wide")
st.title("🏭 Manual Data Entry: Machine Output Predictor")
st.write("Enter the machine settings below, and the AI will predict the Parts Per Hour.")

# We create 3 columns so the webpage looks neat and organized
col1, col2, col3 = st.columns(3)

with col1:
    Injection_Temperature = st.number_input("Injection Temperature", value=220.0)
    Injection_Pressure = st.number_input("Injection Pressure", value=130.0)
    Cycle_Time = st.number_input("Cycle Time", value=30.0)
    Cooling_Time = st.number_input("Cooling Time", value=12.0)
    Material_Viscosity = st.number_input("Material Viscosity", value=300.0)
    Ambient_Temperature = st.number_input("Ambient Temperature", value=25.0)

with col2:
    Machine_Age = st.number_input("Machine Age (years)", value=5.0)
    Operator_Experience = st.number_input("Operator Experience (years)", value=10.0)
    Maintenance_Hours = st.number_input("Maintenance Hours", value=50)
    Temperature_Pressure_Ratio = st.number_input("Temp/Pressure Ratio", value=1.6)
    Total_Cycle_Time = st.number_input("Total Cycle Time", value=42.0)
    Efficiency_Score = st.number_input("Efficiency Score", value=0.05)
    Machine_Utilization = st.number_input("Machine Utilization", value=0.5)

with col3:
    # Use dropdown boxes for text data
    Shift = st.selectbox("Shift", ["Day", "Evening", "Night"])
    Machine_Type = st.selectbox("Machine Type", ["Type_A", "Type_B", "Type_C"])
    Material_Grade = st.selectbox("Material Grade", ["Economy", "Standard", "Premium"])
    Day_of_Week = st.selectbox("Day of Week", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])

# The Predict Button
st.write("---") # Draws a line on the screen
if st.button("Predict Parts Per Hour", type="primary"):
    
    # 1. Gather all the typed inputs into a dictionary
    input_data = {
        "Timestamp": ["01-01-2023 00:00"], # Dummy date because our AI drops it anyway
        "Injection_Temperature": [Injection_Temperature],
        "Injection_Pressure": [Injection_Pressure],
        "Cycle_Time": [Cycle_Time],
        "Cooling_Time": [Cooling_Time],
        "Material_Viscosity": [Material_Viscosity],
        "Ambient_Temperature": [Ambient_Temperature],
        "Machine_Age": [Machine_Age],
        "Operator_Experience": [Operator_Experience],
        "Maintenance_Hours": [Maintenance_Hours],
        "Shift": [Shift],
        "Machine_Type": [Machine_Type],
        "Material_Grade": [Material_Grade],
        "Day_of_Week": [Day_of_Week],
        "Temperature_Pressure_Ratio": [Temperature_Pressure_Ratio],
        "Total_Cycle_Time": [Total_Cycle_Time],
        "Efficiency_Score": [Efficiency_Score],
        "Machine_Utilization": [Machine_Utilization]
    }
    
    # 2. Convert it into a Pandas table
    df = pd.DataFrame(input_data)
    
    # 3. ---> THIS IS THE FIX <---
    # Convert the table into text, and then encode it into "bytes" so the API accepts it
    csv_text = df.to_csv(index=False)
    csv_buffer = io.BytesIO(csv_text.encode('utf-8'))
    
    # Package it exactly how your API expects it
    files = {"file": ("manual_input.csv", csv_buffer, "text/csv")}
    
    with st.spinner("Asking the AI on Render..."):
       with st.spinner("Asking the AI on Render..."):
        try:
            # 4. Send the secret CSV to your live API
            response = requests.post(API_URL, files=files)
            
            if response.status_code == 200:
                result = response.json()
                
                # ---> THE GENIUS FIX <---
                # Instead of guessing the label, we just look for the list of numbers!
                prediction = None
                for key, value in result.items():
                    if type(value) is list and len(value) > 0:
                        prediction = value[0]
                        break
                
                if prediction is not None:
                    # 5. Show the result in a big, beautiful box
                    st.success("Success! Cloud AI calculation complete.")
                    st.metric(label="Predicted Parts Per Hour", value=f"{prediction:.2f} parts")
                else:
                    # If it fails, it will print exactly what the API sent so we can fix it!
                    st.error(f"Could not find the number. The API said: {result}")
                
            else:
                st.error("Error connecting to the API. Is your Render server awake?")
                
        except Exception as e:
            st.error(f"Something went wrong: {e}")