from flask import Flask, render_template
from flask_googlemaps import GoogleMaps
app = Flask(__name__)
GoogleMaps(app)

@app.route('/map')
def map():
    return render_template('template.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9898, debug=True)