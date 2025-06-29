from flask import Flask, request, jsonify
from flask_cors import CORS # Import CORS
import joblib
import pandas as pd
import numpy as np
import requests # For making HTTP requests to the weather API

# Initialize the Flask application
app = Flask(__name__)
# Enable CORS for all routes, allowing frontend to make requests
CORS(app)

# --- Configuration ---
# IMPORTANT: Replace 'YOUR_OPENWEATHERMAP_API_KEY' with your actual key
OPENWEATHER_API_KEY = '5f918a93d72037eacfd6fcf081fc9b2b'
OPENWEATHER_BASE_URL = 'http://api.openweathermap.org/data/2.5/weather?'

# --- Load the trained model ---
try:
    model = joblib.load('weather_model.joblib')
    print("Model 'weather_model.joblib' loaded successfully.")
except FileNotFoundError:
    print("Error: 'weather_model.joblib' not found. Please run 'train_and_save_model.py' first.")
    model = None
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# Define the expected features order for the model
FEATURES_ORDER = ['Max_Temp_Today', 'Min_Temp_Today', 'Humidity_Today', 'Wind_Speed_Today', 'Pressure_Today']

@app.route('/')
def home():
    return "Weather Prediction Backend is running. Send POST request to /predict_live"

@app.route('/predict_live', methods=['POST'])
def predict_live():
    if model is None:
        return jsonify({'error': 'ML Model not loaded. Backend misconfiguration.'}), 500
    if not OPENWEATHER_API_KEY or OPENWEATHER_API_KEY == 'YOUR_OPENWEATHERMAP_API_KEY':
        return jsonify({'error': 'OpenWeatherMap API Key is not configured in app.py'}), 500

    try:
        data = request.get_json(force=True)
        city_name = data.get('city')

        if not city_name:
            return jsonify({'error': 'City name not provided.'}), 400

        # --- Fetch live weather data from OpenWeatherMap ---
        params = {
            'q': city_name,
            'appid': OPENWEATHER_API_KEY,
            'units': 'metric' # Get temperature in Celsius
        }
        weather_response = requests.get(OPENWEATHER_BASE_URL, params=params)
        weather_response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        weather_data = weather_response.json()

        # Extract features required by the model
        # OpenWeatherMap provides current temperature, min/max for the day, humidity, wind, pressure
        # We'll use current 'temp_max' and 'temp_min' from the 'main' object for Max_Temp_Today and Min_Temp_Today
        # Note: For highly accurate "Today's Max/Min", you'd need a more advanced API or accumulation,
        # but for a proof-of-concept, using the daily summary from OpenWeatherMap is common.
        extracted_features = {
            'Max_Temp_Today': weather_data['main']['temp_max'], # Daily max temp
            'Min_Temp_Today': weather_data['main']['temp_min'], # Daily min temp
            'Humidity_Today': weather_data['main']['humidity'],
            'Wind_Speed_Today': weather_data['wind']['speed'], # Wind speed in m/s, but 'units=metric' converts to km/h
            'Pressure_Today': weather_data['main']['pressure']
        }

        # Convert wind speed from m/s to km/h if OpenWeatherMap provides m/s by default
        # With 'units=metric', it should already be km/h or similar, but good to double check API docs.
        # OpenWeatherMap's 'metric' unit for wind speed is meters/sec. Let's convert to km/h for consistency if needed.
        # Assuming our model's 'Wind_Speed_Today' was trained on km/h as in the synthetic data.
        extracted_features['Wind_Speed_Today'] = extracted_features['Wind_Speed_Today'] * 3.6 # m/s to km/h

        # Prepare data for prediction, ensuring correct order and format
        input_values = []
        for feature in FEATURES_ORDER:
            input_values.append(extracted_features[feature])

        input_array = np.array(input_values).reshape(1, -1)

        # Make prediction
        prediction = model.predict(input_array)[0]

        # Return the prediction and the fetched data for display
        return jsonify({
            'predicted_temp': prediction,
            'fetched_data': extracted_features # Send back the data used for prediction
        })

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return jsonify({'error': 'City not found. Please check the spelling.'}), 404
        return jsonify({'error': f'Weather API error: {e.response.status_code} - {e.response.text}'}), 500
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'Network error. Could not connect to Weather API.'}), 500
    except KeyError as e:
        return jsonify({'error': f'Error parsing weather data: Missing expected field {e}.'}), 500
    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {e}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
