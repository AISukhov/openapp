from flask import Flask, request
import request_handler

app = Flask(__name__)
MyW = request_handler.WeatherView()


@app.route("/weather/<string:city>")
def user_query(city, unit='C'):
    # decorator gets city name
    # while request dictionary handles "unit" key
    unit = request.args.get('unit', unit)
    message = MyW.get_weather(city, unit)
    return message


if __name__ == '__main__':
    app.run(debug=True, port=5050)
