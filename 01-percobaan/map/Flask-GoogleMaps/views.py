from flask import Flask, render_template
from flask_googlemaps import GoogleMaps

app = Flask(__name__, template_folder=".")
GoogleMaps(app)

@app.route("/")
def testing():
    # creating a map in the view
    return render_template('testing.html')


@app.route("/mapview")
def mapview():
    # creating a map in the view
    return render_template('example.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9999 ,debug=True)