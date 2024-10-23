import sqlite3
from datetime import datetime
from config import DB_NAME


def create_db():
    """Initialize the database and create tables if they do not exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS daily_summary (
        city TEXT,
        timestamp DATETIME,
        avg_temp REAL,
        max_temp REAL,
        min_temp REAL,
        dominant_condition TEXT,
        wind_speed REAL,
        wind_direction TEXT,
        visibility INTEGER,
        cloudiness INTEGER
    )
    ''')
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY,
            city TEXT,
            message TEXT,
            timestamp DATETIME
        )
    """)
    conn.commit()
    conn.close()


def store_daily_summary(city, timestamp, avg_temp, max_temp, min_temp, dominant_condition,
                        wind_speed, wind_direction, visibility, cloudiness):
   
    """Store a daily summary in the database.

    Parameters:
        city (str): City name
        timestamp (datetime): Timestamp of the summary
        avg_temp (float): Average temperature
        max_temp (float): Maximum temperature
        min_temp (float): Minimum temperature
        dominant_condition (str): Dominant weather condition
        wind_speed (float): Average wind speed
        wind_direction (str): Average wind direction
        visibility (int): Average visibility
        cloudiness (int): Average cloudiness
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO daily_summary (city, timestamp, avg_temp, max_temp, min_temp, dominant_condition,
    wind_speed, wind_direction, visibility, cloudiness)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (city, timestamp.isoformat(), avg_temp, max_temp, min_temp, dominant_condition,
          wind_speed, wind_direction, visibility, cloudiness))
    conn.commit()
    conn.close()


def get_daily_summaries():

    """Retrieve all daily summaries from the database and format them for display.

    Returns:
        A list of tuples, each containing the city, timestamp, average temperature,
        maximum temperature, minimum temperature, dominant condition, average wind
        speed, average wind direction, average visibility, and average cloudiness.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT city, timestamp, avg_temp, max_temp, min_temp, dominant_condition, wind_speed, wind_direction, visibility, cloudiness
        FROM daily_summary
        ORDER BY timestamp DESC
    ''')
    rows = cursor.fetchall()
    conn.close()
    
    formatted_rows = []
    for row in rows:
        city, timestamp, avg_temp, max_temp, min_temp, dominant_condition, wind_speed, wind_direction, visibility, cloudiness = row
        
        # Parse and reformat the timestamp to 'YYYY-MM-DD 00:00:00'
        formatted_timestamp = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f").strftime("%Y-%m-%d %H:%M:%S")
        
        # Append formatted data
        formatted_rows.append((
            city, formatted_timestamp, avg_temp, max_temp, min_temp, dominant_condition, wind_speed, wind_direction, visibility, cloudiness
        ))

    return formatted_rows


def store_alert(city, message, timestamp):

    """
    Stores an alert message in the database for a specific city.

    Parameters:
        city (str): The name of the city where the alert is triggered.
        message (str): The alert message to be stored.
        timestamp (datetime): The timestamp when the alert is created.

    This function ensures the 'alerts' table exists in the database and inserts a new alert record.
    """
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY,
            city TEXT,
            message TEXT,
            timestamp DATETIME
        )
    """)
    cursor.execute("""
        INSERT INTO alerts (city, message, timestamp)
        VALUES (?, ?, ?)
    """, (city, message, timestamp.isoformat()))
    conn.commit()
    conn.close()


def get_alerts_summaries():
  
    """
    Retrieves all alert summaries from the database in descending order of timestamp.

    Returns a list of tuples containing the city name, alert message, and timestamp.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT city, message, timestamp FROM alerts ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows


create_db()
