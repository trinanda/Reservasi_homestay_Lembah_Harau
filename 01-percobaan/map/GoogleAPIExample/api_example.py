from flask import Flask, render_template, jsonify
import requests
from key import GOOGLE_MAP_API
from shapely import wkb, wkt
from binascii import unhexlify
app = Flask(__name__)

search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
details_url = "https://maps.googleapis.com/maps/api/place/details/json"

@app.route("/", methods=["GET"])
def retreive():
	wkt_number = '01010000001100008890285940FF55ED493B85CCBF'
	binary = unhexlify(wkt_number)
	point = wkb.loads(binary)
	longitude = str(point.y)
	latitude = str(point.x)

	kodinat = longitude+','+latitude

	return render_template('layout.html', KORDINAT=kodinat)

@app.route("/sendRequest/<string:query>")
def results(query):
	search_payload = {"key":GOOGLE_MAP_API, "query":query}
	search_req = requests.get(search_url, params=search_payload)
	search_json = search_req.json()

	place_id = search_json["results"][0]["place_id"]

	details_payload = {"key":GOOGLE_MAP_API, "placeid":place_id}
	details_resp = requests.get(details_url, params=details_payload)
	details_json = details_resp.json()

	url = details_json["result"]["url"]
	return jsonify({'result' : url})


if __name__ ==  "__main__":
    app.run(debug=True)