from flask import Flask, request
import request_handler

app = Flask(__name__)
MyW = request_handler.WeatherView()


@app.route("/weather/<city>")
def user_query(city):
    # decorator gets city name
    # while request dictionary handles "unit" key
    unit = request.args['unit']
    message = MyW.get_weather(city, unit)
    return message


if __name__ == '__main__':
    app.run(debug=True, port=5050)
