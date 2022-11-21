from flask import Flask, request
import firebase_admin
from firebase_admin import credentials, firestore
from flask import jsonify
import pygeohash as pgh
from geopy import distance

app = Flask(__name__)

# cred = credentials.Certificate('/Users/aj/Downloads/bright-pro-firebase-adminsdk-1ao7r-920e09b64c.json')
cred = credentials.Certificate('./bright-pro-firebase-adminsdk-1ao7r-920e09b64c.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
doc_ref = db.collection(u'venues')


@app.route("/")
def hello():
    return "Please type your query in URL"

@app.route("/search", methods=['GET'])
def index():
    args = request.args
    if 'name' in args:
        name = args.get('name')
        ml = doc_ref.where(u'restaurant_name', u'==', name)
        docs = ml.stream()
        out_li = []
        for doc in docs:
            out_li.append(doc.to_dict())

    elif 'rating' in args:
        rating = args.get('rating')
        ml = doc_ref.where(u'restaurant_name', u'>=', rating)
        docs = ml.stream()
        dummy = []

        for doc in docs:
            dummy.append(doc.to_dict())

        out_li = sorted(dummy, key=lambda y: y['restaurant_rating'], reverse=True)

    elif 'price_type' in args:
        price = args.get('price_type')
        ml = doc_ref.where(u'price_type', u'==', price)
        docs = ml.stream()
        dummy = []

        for doc in docs:
            dummy.append(doc.to_dict())

        out_li = sorted(dummy, key=lambda y: y['restaurant_name'], reverse=False)

    elif ('latitude' in args) and ('longitude' in args):
        lat = args.get('latitude')
        lon = args.get('longitude')

        search_geo = pgh.encode(float(lat), float(lon), precision=5)

        ml = doc_ref.where(u'geohash', u'==', search_geo)
        docs = ml.stream()
        dummy = []
        ind = {}
        out_li = []

        for doc in docs:
            dummy.append(doc.to_dict())

        for idx, dummy_item in enumerate(dummy):
            key = distance.distance((lat,lon), (dummy_item['lat'], dummy_item['lon']))
            value = idx
            ind[key] = value

        ind_sorted = sorted(ind.items())

        for z in ind_sorted:
            out_li.append(dummy[z[1]])

    else:
        return "Invalid Input"




    return jsonify(results = out_li)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)
