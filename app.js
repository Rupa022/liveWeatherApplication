document.addEventListener('DOMContentLoaded', () => {
    // Get references to HTML elements
    const cityNameInput = document.getElementById('cityName');
    const predictBtn = document.getElementById('predictBtn');
    const resultDiv = document.getElementById('result');
    const predictedTemperatureSpan = document.getElementById('predictedTemperature');
    const fetchedConditionsP = document.getElementById('fetchedConditions');
    const messageBox = document.getElementById('messageBox');
    const messageText = document.getElementById('messageText');
    const loadingIndicator = document.getElementById('loadingIndicator');

    // Function to display messages (errors, success messages)
    function showMessage(message, type = 'error') {
        messageText.textContent = message;
        messageBox.classList.remove('hidden', 'bg-red-100', 'bg-green-100', 'text-red-800', 'text-green-800');
        if (type === 'error') {
            messageBox.classList.add('bg-red-100', 'text-red-800');
        } else {
            messageBox.classList.add('bg-green-100', 'text-green-800');
        }
        resultDiv.classList.add('hidden'); // Hide result when a message is shown
        loadingIndicator.classList.add('hidden'); // Hide loading
    }

    // Function to hide messages
    function hideMessage() {
        messageBox.classList.add('hidden');
    }

    // Function to show loading
    function showLoading() {
        loadingIndicator.classList.remove('hidden');
        resultDiv.classList.add('hidden');
        hideMessage();
    }

    // Function to hide loading
    function hideLoading() {
        loadingIndicator.classList.add('hidden');
    }

    // Function to handle prediction request
    predictBtn.addEventListener('click', async () => {
        const cityName = cityNameInput.value.trim();

        if (cityName === '') {
            showMessage('Please enter a city name.');
            return;
        }

        showLoading(); // Show loading indicator

        // Send city name to the backend API
        try {
            // Adjust the URL if your Flask server runs on a different port or host
            const response = await fetch('http://127.0.0.1:5000/predict_live', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ city: cityName }),
            });

            const result = await response.json();
            hideLoading(); // Hide loading indicator once response is received

            if (response.ok) {
                // Display the prediction and fetched conditions
                predictedTemperatureSpan.textContent = `Predicted Max Temperature for Tomorrow: ${result.predicted_temp.toFixed(2)}°C`;
                fetchedConditionsP.textContent = `(Based on today's Max: ${result.fetched_data.Max_Temp_Today}°C, Min: ${result.fetched_data.Min_Temp_Today}°C, Humidity: ${result.fetched_data.Humidity_Today}%, Wind: ${result.fetched_data.Wind_Speed_Today} km/h, Pressure: ${result.fetched_data.Pressure_Today} hPa)`;
                resultDiv.classList.remove('hidden');
            } else {
                // Handle errors from the backend
                showMessage(`Prediction error: ${result.error || 'Something went wrong.'}`);
            }
        } catch (error) {
            hideLoading(); // Hide loading indicator on error
            // Handle network or other unexpected errors
            console.error('Fetch error:', error);
            showMessage('Could not connect to the prediction server. Please ensure the backend is running and you have internet access.');
        }
    });
});
