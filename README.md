# Real-Time Data Processing System for Weather Monitoring with Rollups and Aggregates
## Introduction

This project is part of an assignment for securing an internship as a backend developer. The **Real-Time Data Processing System for Weather Monitoring with Rollups and Aggregates** continuously fetches weather data for multiple cities, stores daily summaries in a database, and triggers weather alerts based on configurable thresholds. The project showcases my backend development skills using Python, Flask, and REST APIs.

---

## Project Overview

The **Real-Time Data Processing System for Weather Monitoring with Rollups and Aggregates** is a Flask-based application that:

1. Retrieves real-time weather data from the OpenWeatherMap API every 5 minutes.
2. Stores daily summaries, including temperature, wind speed, visibility, and weather conditions in a SQLite database.
3. Allows users to set alert thresholds for temperature and other weather parameters, with notifications triggered when thresholds are breached.
4. Displays historical weather trends and summaries on the frontend with a user-friendly interface.

---

## Features

- Fetch real-time weather data for multiple cities.
- Convert temperatures from Kelvin to Celsius.
- Store daily weather summaries in a database.
- Trigger alerts when specific weather thresholds are breached.
- Historical data visualization for daily summaries (graphs for temperature, wind speed, etc.).
- Dynamic frontend interaction using JavaScript to fetch data from the database.

---

## Screenshots

---

### Weather Monitor Dashboard


![Weather Monitor Dashboard](https://github.com/user-attachments/assets/df7fef12-822d-4400-9881-f66a5ceb36d2)

### Historical Weather Data

![Historical Weather Data](https://github.com/user-attachments/assets/d4823966-f8a6-4fbf-8893-776ad9ed621f)

### Weather Alerts 

**Threshold was set to 15°C for testing**

![Weather Alerts](https://github.com/user-attachments/assets/6e1776f4-34ad-491f-9ce5-1b0d5fe76dec)

**Alerts on Console**

![image](https://github.com/user-attachments/assets/573b3fad-0746-4117-bb37-e47bd46a5081)

---

## Technologies Used

- **Python** (Backend Development)
- **Flask** (Web Framework)
- **JavaScript** (Client-Side Data Fetching)
- **SQLite** (Database)
- **HTML/CSS** (Frontend Design)
- **OpenWeatherMap API** (Weather Data Retrieval)

---

## Project Structure

        Weather_Monitor_Project/
        │
        ├── app.py                       # Main Flask application
        ├── config.py                    # Configuration settings (e.g., API key, cities, thresholds)
        ├── requirements.txt             # Required Python libraries
        ├── weather/
        │   ├── aggregate.py             # Daily summary calculations
        │   ├── conversion.py            # Temperature conversion functions (Kelvin to Celsius)
        │   ├── fetch.py                 # Fetch weather data from OpenWeatherMap API
        │   ├── database.py              # Database operations (store summaries, alerts, etc.)
        │
        ├── templates/
        │   ├── index.html               # Frontend UI for displaying weather summaries
        │   ├── result.html              # UI for displaying detailed results
        │
        ├── static/
        │   ├── style.css                # Stylesheet for UI
        │   ├── script.js                # JavaScript for dynamic interactions
        │
        ├── tests/                       # Test cases for all functionalities
        │   ├── tests.py                 # Unit tests for fetching data, storing summaries, and alerting
        │
        └── README.md                    # Project README file (you are reading this)

---

## Setup and Installation

To set up and run this project locally, follow these steps:

1. **Clone the Repository**:
   ```git
   git clone https://github.com/your-username/weather-monitor-project.git
   ```
   ```cmd
   cd weather-monitor-project
   ```

- Create and Activate a Virtual Environment:
    ```python
    python3 -m venv ProjectEnv
      
    source ProjectEnv/bin/activate  # On Windows: ProjectEnv\Scripts\activate
    ```
- Install the Dependencies:
    ```python
    pip install -r requirements.txt
    ```
- Configure API Keys and Settings:

  Open config.py and update it with your API key from OpenWeatherMap.
  Set up the cities for which you want to monitor the weather.

  Example of config.py:

  ```python
  API_KEY = 'your_api_key_here'  # Your OpenWeatherMap API key
  CITIES = ['Delhi', 'Mumbai', 'Chennai']  # Cities to monitor
  INTERVAL = 300  # Update interval in seconds

  ALERT_THRESHOLDS = {
      'temperature': {'value': 35, 'consecutive_count': 2},  # Temp alert settings
      'conditions': ['Rain', 'Storm']  # Alert conditions
  }
  ```
---

## How to Run

Start the Flask Server:

```python
python app.py
```

Access the Application: Open your browser and visit http://127.0.0.1:5000/ to interact with the frontend, view weather summaries, and set alert configurations.

---

## Database Schema Overview

The system utilizes an SQLite database to store data in two main areas: **daily summaries** of weather data and **alerts** for specific weather conditions.

### Daily Summaries

- **Purpose**: This part of the database stores aggregated weather data for each city on a daily basis.
- **Key Data Points**:
  - **City Name**: Identifies the location of the weather data.
  - **Timestamps**: Records the date and time for which the weather data applies, typically set to midnight of the day.
  - **Temperature Metrics**: Includes average, maximum, and minimum temperatures, converted to Celsius.
  - **Weather Condition**: Describes the predominant weather condition (e.g., Clear, Rain).
  - **Wind Information**: Captures wind speed and direction.
  - **Visibility**: Measures how far one can see, in meters.
  - **Cloudiness**: Indicates the percentage of cloud cover.

### Alerts

- **Purpose**: This component handles notifications about severe weather conditions.
- **Key Data Points**:
  - **City Name**: Specifies the location related to the alert.
  - **Alert Message**: Contains the text of the alert, detailing the nature of the weather warning.
  - **Timestamps**: Records when the alert was issued.

---

## Testing

- Unit tests are provided to ensure the project runs as expected. These tests cover weather data fetching, summary calculations, and alert storage.

  Run the Tests:

  ```python
  python -m unittest tests/tests.py
  ```

- Tests include:

  - Weather Data Fetching: Ensures data is correctly fetched from the API.
  - Temperature Conversion: Verifies Kelvin-to-Celsius conversion logic.
  - Daily Summary Calculation: Confirms the daily weather summary is correctly calculated.
  - Alerting: Tests the alert system when thresholds are breached.

---

## Contact Information

If you have any questions or feedback about the project, feel free to contact me:

<a href="mailto:your_email@example.com">
    <img src="https://skillicons.dev/icons?i=gmail" alt="Gmail" style="width: 24px; height: 24px; margin-right: 10px;">
</a>
<a href="https://www.linkedin.com/in/yourprofile">
    <img src="https://skillicons.dev/icons?i=linkedin" alt="LinkedIn" style="width: 24px; height: 24px;">
</a>

---
