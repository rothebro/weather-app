from flask import Flask, request
import requests
import os
app = Flask(__name__)

api_key = 'd5881f7a33e94269ba225856250608'

@app.route("/", methods=["GET"])
def home():
    city = request.args.get('city')
    days = request.args.get('days')

    html = """
    <h3>Check the forecast</h3>

        <form method="POST">
            <input type="text" name="city" placeholder="Enter a city" style="width: 150px; margin-right: 5px;">
            <input type="number" name="days" placeholder="1–10 days" min="1" max="10" style="width: 120px; margin-right: 5px;">
            <input type="submit" value="Get Weather">
        </form>
    """

    if city and days:
        try:
            days = int(days)
            if not (1 <= days <= 10):
                html += "<p>Please enter a number between 1 and 10 for days.</p>"
                return html

            url = "http://api.weatherapi.com/v1/forecast.json"
            params = {'key': api_key, 'q': city, 'days': days}

            r = requests.get(url, params=params)

            if r.status_code == 200:
                data = r.json()
                forecast_days = data['forecast']['forecastday']

                html += f"<h1>{days}-Day Forecast for {city.title()}</h1>"
                for day in forecast_days:
                    date = day['date']
                    avg_temp = day['day']['avgtemp_c']
                    condition = day['day']['condition']['text']
                    chance_of_rain = day['day']['daily_chance_of_rain']
                    html += f"<p><b>{date}:</b> {avg_temp}°C, {condition}, Rain: {chance_of_rain}%</p>"
            else:
                html += f"<p>Error fetching weather: {r.status_code}</p>"

        except ValueError:
            html += "<p>Days must be a number.</p>"
    elif city or days:
        html += "<p>Please fill in both fields.</p>"

    return html

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use PORT from Render, or default to 5000
    app.run(host="0.0.0.0", port=port)

