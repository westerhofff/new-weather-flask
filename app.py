from flask import Flask, request, render_template
import requests


app = Flask(__name__)

def get_weather(location, unit='metric'):
    api_key = 'd423431d8d6f801ecda80e0856ccc2f3'
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units={unit}"
        res = requests.get(url)
        data = res.json()
        return data
    except requests.exceptions.RequestException as e:
        return {"error": "Error connecting to the OpenWeather API: " + str(e)}


@app.route('/', methods=['GET', 'POST'])
def weather():
    if request.method == 'POST':
        location = request.form['location']
        unit = request.form['unit']
        weather_data = get_weather(location, unit)
        if "error" in weather_data:
            return render_template('error.html', error=weather_data["error"])
        if weather_data['cod'] != 200:
            return render_template('error.html', error=weather_data['message'])
        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        pressure = weather_data['main']['pressure']
        return render_template('weather.html', temp=temp, humidity=humidity, pressure=pressure)
    return render_template('weather.html')




if __name__ == '__main__':
    app.run(debug=True)
