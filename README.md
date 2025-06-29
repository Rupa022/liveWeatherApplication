# liveWeatherApplication
Live Weather Prediction App (Full-Stack with ML &amp; API Integration) Developed a full-stack application leveraging Python (Flask) and web technologies to predict tomorrow's temperature, integrating a machine learning model with a real-time weather API. Demonstrated expertise in ML deployment, API consumption, and dynamic web development.
Live Weather Prediction Application
Overview
This project is a full-stack web application that predicts tomorrow's maximum temperature for a given city. It leverages a machine learning model, a Python Flask backend for API integration and serving predictions, and a dynamic frontend for user interaction. The application demonstrates an end-to-end Machine Learning Operations (MLOps) pipeline from model training to live deployment and data consumption.

Features
Temperature Prediction: Predicts tomorrow's maximum temperature based on today's weather conditions.

Live Data Fetching: Automatically retrieves current weather data for any specified city using the OpenWeatherMap API.

Machine Learning Integration: Utilizes a pre-trained Linear Regression model (or other Scikit-learn regressors) for forecasting.

User-Friendly Frontend: An intuitive web interface built with HTML, Tailwind CSS, and JavaScript.

Backend API: A Python Flask server acts as an intermediary, handling API requests and serving model predictions.

Modular Design: Separate components for model training, backend API, and frontend.

Technologies Used
Machine Learning:

Python

scikit-learn: For building and training the regression model.

pandas & numpy: For data manipulation and numerical operations.

joblib: For serializing and deserializing the trained ML model.

Backend:

Python

Flask: Web framework for creating the REST API.

flask-cors: For handling Cross-Origin Resource Sharing.

requests: For making HTTP requests to external APIs (OpenWeatherMap).

Frontend:

HTML5: Structure of the web page.

Tailwind CSS: Utility-first CSS framework for styling and responsive design.

JavaScript (ES6+): For dynamic behavior and interacting with the backend API.

External API:

OpenWeatherMap API: Used to fetch real-time weather data.

How It Works
Model Training (train_and_save_model.py): A simple machine learning model (Linear Regression) is trained on a synthetic dataset of historical weather conditions to learn the relationship between today's weather and tomorrow's maximum temperature. The trained model is then saved as weather_model.joblib.

Backend Server (app.py):

A Flask server is launched, which loads the pre-trained weather_model.joblib into memory.

It exposes a /predict_live API endpoint.

When this endpoint receives a city name from the frontend, it calls the OpenWeatherMap API to get the current weather data for that city.

The fetched data is then fed into the loaded ML model to generate a prediction for tomorrow's maximum temperature.

The prediction, along with the fetched input data, is sent back to the frontend.

Frontend Interface (index.html, app.js):

The user inputs a city name into the web interface.

JavaScript handles the button click, sends the city name to the Flask backend's /predict_live endpoint.

Upon receiving the prediction, the JavaScript updates the UI to display the forecasted temperature and the weather conditions used for the prediction.

Setup and Installation
Follow these steps to get the application running on your local machine.

1. Prerequisites
Python 3.8+

pip (Python package installer)

2. Get Your OpenWeatherMap API Key
Go to OpenWeatherMap and sign up for a free account.

Once logged in, navigate to the "API keys" tab in your profile.

Copy your generated API key. You will need this in the next step.

3. Clone the Repository (or create files)
Create a new folder (e.g., LiveWeatherApp) and save the following files within it:

index.html

app.js

app.py

train_and_save_model.py

4. Configure Your API Key
Open app.py and replace 'YOUR_OPENWEATHERMAP_API_KEY' with your actual API key obtained from OpenWeatherMap:

OPENWEATHER_API_KEY = 'YOUR_OPENWEATHERMAP_API_KEY' # <--- Paste your key here

5. Install Dependencies
Open your terminal or command prompt, navigate to your LiveWeatherApp folder, and install the required Python libraries:

cd path/to/your/LiveWeatherApp # Replace with your actual folder path
pip install pandas numpy scikit-learn flask flask-cors requests joblib

6. Train and Save the ML Model
In the same terminal window, run the training script:

python train_and_save_model.py

This will create a file named weather_model.joblib in your LiveWeatherApp directory. This file contains your trained machine learning model.

7. Start the Flask Backend Server
Keep the terminal window open from the previous step, or open a new one and navigate to your LiveWeatherApp folder. Then, start the Flask server:

python app.py

You should see output indicating that the Flask app is running, typically on http://127.0.0.1:5000/. Keep this terminal window open as long as you want the backend to be running.

8. Open the Frontend Application
Open your web browser (Chrome, Firefox, Edge, etc.) and open the index.html file. You can do this by:

Typing file:///path/to/your/LiveWeatherApp/index.html in the address bar.

Or, simply by double-clicking the index.html file in your file explorer.

Usage
Enter a city name (e.g., "London", "New York", "Delhi") in the input field on the web page.

Click the "Get Prediction for Tomorrow" button.

The application will display the predicted maximum temperature for tomorrow, along with the current weather conditions it fetched for the input city.
