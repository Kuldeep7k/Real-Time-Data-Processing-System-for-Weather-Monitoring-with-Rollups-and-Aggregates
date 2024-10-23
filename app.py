from flask import Flask, render_template, jsonify
import pandas as pd
from apscheduler.schedulers.background import BackgroundScheduler
from weather.database import create_db, get_daily_summaries, get_alerts_summaries
from weather.aggregate import fetch_and_aggregate
import config
import logging
import plotly.express as px

app = Flask(__name__)
scheduler = BackgroundScheduler()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Dictionary to track consecutive breaches for each city
consecutive_breaches = {city: 0 for city in config.CITIES}


@app.route('/')
def index():
    # Fetch historical summaries from the database
    """
    This function fetches historical summaries from the database, creates DataFrames for historical data with temperature conversion, and plots temperature and additional data graphs for display on the frontend.

    Returns:
        str: The rendered HTML template for the index page with temperature and additional data graphs.
    """

    historical_summaries = get_daily_summaries()

    # Create DataFrame for historical data with temperature conversion
    historical_data = []
    additional_data = []  # For the second graph (e.g., wind speed)

    for row in historical_summaries:
        city, timestamp, avg_temp, max_temp, min_temp, condition, wind_speed, wind_direction, visibility, cloudiness = row

        # Directly add row data without grouping
        historical_data.append({
            'timestamp': timestamp,
            'avg_temp': avg_temp,
            'max_temp': max_temp,
            'city': city,
        })

        # Collect additional data for the second graph
        additional_data.append({
            'timestamp': timestamp,
            'wind_speed': wind_speed,
            'visibility': visibility,
            'cloudiness': cloudiness,
            'city': city,
            'condition': condition,
        })

    # Create DataFrames
    historical_df = pd.DataFrame(historical_data)
    historical_df['timestamp'] = pd.to_datetime(historical_df['timestamp'])

    additional_df = pd.DataFrame(additional_data)
    additional_df['timestamp'] = pd.to_datetime(additional_df['timestamp'])

    # Plot the temperature comparison graph
    if 'timestamp' in historical_df.columns and 'avg_temp' in historical_df.columns:
        fig_temp = px.line(historical_df, x='timestamp', y='avg_temp', color='city',
                           title="Average Temperature Trend Across Indian Metros",
                           labels={'timestamp': 'Time',
                                   'avg_temp': 'Temperature (°C)'},
                           template='plotly_dark')  # Set dark theme

        # Update traces for better visibility
        fig_temp.update_traces(
            line=dict(width=2, dash='solid'), mode='lines+markers')
        fig_temp.update_layout(
            title_font=dict(color='white'),
            legend_title_font=dict(color='white'),
            xaxis_title_font=dict(color='white'),
            yaxis_title_font=dict(color='white'),
            xaxis=dict(color='white'),
            yaxis=dict(color='white'),
        )

        # Convert temperature figure to HTML
        temp_graph_html = fig_temp.to_html(full_html=False)

    else:
        temp_graph_html = "No historical temperature data available"

    # Plot the additional data graph (e.g., wind speed)
    if 'timestamp' in additional_df.columns and 'wind_speed' in additional_df.columns:
        fig_additional = px.line(additional_df, x='timestamp', y='wind_speed', color='city',
                                 title="Wind Speed Trend Across Indian Metros",
                                 labels={'timestamp': 'Time',
                                         'wind_speed': 'Wind Speed (m/s)'},
                                 template='plotly_dark',
                                 hover_data=['condition'])

        fig_additional.update_traces(
            line=dict(width=2, dash='solid'), mode='lines+markers')
        fig_additional.update_layout(
            title_font=dict(color='white'),
            legend_title_font=dict(color='white'),
            xaxis_title_font=dict(color='white'),
            yaxis_title_font=dict(color='white'),
            xaxis=dict(color='white'),
            yaxis=dict(color='white'),
        )

        # Convert additional figure to HTML
        additional_graph_html = fig_additional.to_html(full_html=False)

    else:
        additional_graph_html = "No additional data available"

    return render_template('index.html', temp_graph_html=temp_graph_html, additional_graph_html=additional_graph_html)


@app.route('/historical')
def historical():
    """Render a template with historical weather summaries."""

    summaries = get_daily_summaries()
    return render_template('historical.html', summaries=summaries)


@app.route('/api/weather-data')
def api_weather_data():
    # If you no longer want to fetch current weather, you can return an empty JSON
    """Return a JSON array of current weather data for all cities."""
    return jsonify([])


@app.route('/alerts')
def alerts():
    """Render a template with weather alerts summaries.
    Returns a list of tuples, each containing the city, alert message, and timestamp.
    """
    alerts = get_alerts_summaries()
    return render_template('alerts.html', alerts=alerts)


# Fetch initial data when the app starts
create_db()  # Initialize the database
fetch_and_aggregate()

# Schedule the fetch_and_aggregate function every INTERVAL seconds if needed
# Uncomment if you plan to schedule data aggregation
scheduler.add_job(fetch_and_aggregate, 'interval', seconds=config.INTERVAL)

# Start the scheduler if necessary
scheduler.start()

if __name__ == '__main__':
    # Disable reloader when using scheduler
    app.run(debug=True, use_reloader=False)
