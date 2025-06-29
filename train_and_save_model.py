import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
import joblib # Library to save/load Python objects, including scikit-learn models
import os

print("--- Training and Saving Weather Prediction Model ---")

# --- 1. Simulate/Create a Dataset (In a real project, you'd load from a CSV) ---
np.random.seed(42) # for reproducibility

dates = pd.date_range(start='2023-01-01', periods=100)
data = {
    'Date': dates,
    'Max_Temp_Today': np.random.randint(20, 40, size=100) + np.sin(np.arange(100)/10) * 5, # Simulate seasonal variation
    'Min_Temp_Today': np.random.randint(10, 25, size=100) + np.sin(np.arange(100)/10) * 3,
    'Humidity_Today': np.random.randint(40, 90, size=100),
    'Wind_Speed_Today': np.random.uniform(5, 25, size=100),
    'Pressure_Today': np.random.uniform(990, 1020, size=100),
}
df = pd.DataFrame(data)

df['Max_Temp_Tomorrow'] = df['Max_Temp_Today'].shift(-1)
df = df.dropna().reset_index(drop=True)

print("Simulated Weather Data created.")

# --- 2. Define Features (X) and Target (y) ---
features = ['Max_Temp_Today', 'Min_Temp_Today', 'Humidity_Today', 'Wind_Speed_Today', 'Pressure_Today']
target = 'Max_Temp_Tomorrow'

X = df[features]
y = df[target]

# --- 3. Split Data into Training and Testing Sets ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- 4. Initialize and Train the Model ---
model = LinearRegression() # Using Linear Regression as an example
print("\nTraining the Linear Regression model...")
model.fit(X_train, y_train)
print("Model training complete.")

# --- 5. Evaluate the Model's Performance (Optional, but good practice) ---
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"\nModel Evaluation (on Test Set):")
print(f"  Mean Absolute Error (MAE): {mae:.2f}°C")
print(f"  R-squared (R2) Score: {r2:.2f}")


# --- 6. Save the Trained Model ---
model_filename = 'weather_model.joblib'
try:
    joblib.dump(model, model_filename)
    print(f"\nModel successfully saved to '{model_filename}'")
except Exception as e:
    print(f"Error saving model: {e}")

# Verify file creation
if os.path.exists(model_filename):
    print(f"File '{model_filename}' exists and is ready for use by app.py.")
else:
    print(f"Error: Model file '{model_filename}' was not created.")

