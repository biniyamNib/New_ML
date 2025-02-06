import streamlit as st
import requests
import pandas as pd

# Define the API endpoint
FASTAPI_URL = "https://machine-learning-project-bu4q.onrender.com/predict"  # Replace with your FastAPI server URL

# Title of the app
st.title("Rain Prediction App 🌧️")

# Sidebar for user input
st.sidebar.header("User Input Parameters")

# Function to get user input
def get_user_input():
    MinTemp = st.sidebar.slider("Minimum Temperature (°C)", -10.0, 50.0, 15.0)
    MaxTemp = st.sidebar.slider("Maximum Temperature (°C)", -10.0, 50.0, 25.0)
    Rainfall = st.sidebar.slider("Rainfall (mm)", 0.0, 100.0, 0.0)
    Evaporation = st.sidebar.slider("Evaporation (mm)", 0.0, 20.0, 5.0)
    Sunshine = st.sidebar.slider("Sunshine (hours)", 0.0, 15.0, 7.0)
    WindGustDir = st.sidebar.selectbox("Wind Gust Direction", ["N", "NE", "E", "SE", "S", "SW", "W", "NW"])
    WindGustSpeed = st.sidebar.slider("Wind Gust Speed (km/h)", 0.0, 150.0, 40.0)
    WindDir9am = st.sidebar.selectbox("Wind Direction at 9am", ["N", "NE", "E", "SE", "S", "SW", "W", "NW"])
    WindDir3pm = st.sidebar.selectbox("Wind Direction at 3pm", ["N", "NE", "E", "SE", "S", "SW", "W", "NW"])
    WindSpeed9am = st.sidebar.slider("Wind Speed at 9am (km/h)", 0.0, 100.0, 10.0)
    WindSpeed3pm = st.sidebar.slider("Wind Speed at 3pm (km/h)", 0.0, 100.0, 15.0)
    Humidity9am = st.sidebar.slider("Humidity at 9am (%)", 0.0, 100.0, 60.0)
    Humidity3pm = st.sidebar.slider("Humidity at 3pm (%)", 0.0, 100.0, 50.0)
    Pressure9am = st.sidebar.slider("Pressure at 9am (hPa)", 900.0, 1100.0, 1015.0)
    Pressure3pm = st.sidebar.slider("Pressure at 3pm (hPa)", 900.0, 1100.0, 1013.0)
    Cloud9am = st.sidebar.slider("Cloud at 9am (oktas)", 0.0, 9.0, 5.0)
    Cloud3pm = st.sidebar.slider("Cloud at 3pm (oktas)", 0.0, 9.0, 4.0)
    Temp9am = st.sidebar.slider("Temperature at 9am (°C)", -10.0, 50.0, 20.0)
    Temp3pm = st.sidebar.slider("Temperature at 3pm (°C)", -10.0, 50.0, 25.0)
    RainToday = st.sidebar.selectbox("Rain Today", ["No", "Yes"])

    # Create a dictionary to store the user input
    user_data = {
        "MinTemp": MinTemp,
        "MaxTemp": MaxTemp,
        "Rainfall": Rainfall,
        "Evaporation": Evaporation,
        "Sunshine": Sunshine,
        "WindGustDir": WindGustDir,
        "WindGustSpeed": WindGustSpeed,
        "WindDir9am": WindDir9am,
        "WindDir3pm": WindDir3pm,
        "WindSpeed9am": WindSpeed9am,
        "WindSpeed3pm": WindSpeed3pm,
        "Humidity9am": Humidity9am,
        "Humidity3pm": Humidity3pm,
        "Pressure9am": Pressure9am,
        "Pressure3pm": Pressure3pm,
        "Cloud9am": Cloud9am,
        "Cloud3pm": Cloud3pm,
        "Temp9am": Temp9am,
        "Temp3pm": Temp3pm,
        "RainToday": RainToday,
    }

    # Convert the dictionary to a DataFrame
    features = pd.DataFrame(user_data, index=[0])
    return features

# Get user input
user_input = get_user_input()

# Display the user input
st.subheader("User Input Parameters")
st.write(user_input)

# Debug: Print the user input being sent
st.write("User Input to be Sent:", user_input.to_dict(orient="records")[0])

# Make a prediction
if st.button("Predict"):
    try:
        # Convert the DataFrame to a dictionary and send it as JSON
        input_data = user_input.to_dict(orient="records")[0]
        st.write("Data being sent to API:", input_data)

        # Send the user input to the FastAPI server
        response = requests.post(FASTAPI_URL, json=input_data)
        st.write("API Response Status Code:", response.status_code)
        st.write("API Response Content:", response.json())
        response.raise_for_status()

        # Get the prediction result
        prediction = response.json()
        st.subheader("Prediction Result")
        st.write(f"Will it rain tomorrow? **{prediction['prediction']}**")
        st.write(f"Probability of rain: **{prediction['probability']:.2f}**")
    except requests.exceptions.RequestException as e:
        st.error(f"Error making prediction: {e}")