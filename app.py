
# Library import.
from flask import Flask, request
import firebase_admin
from firebase_admin import credentials, firestore
from flask import jsonify
import pygeohash as pgh
from geopy import distance


app = Flask(__name__)

# Your Firebase credentials here.
cred = credentials.Certificate('./bright-pro-firebase-adminsdk-1ao7r-920e09b64c.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
doc_ref = db.collection(u'venues')


# Homepage.
@app.route("/")
def hello():
    return "Please type your query in URL"

# Search endpoints.
@app.route("/search", methods=['GET'])
def index():
    args = request.args

    # /search?name  -- Returns a single document.
    if 'name' in args:
        name = args.get('name')

        # Firebase query.
        ml = doc_ref.where(u'restaurant_name', u'==', name)
        docs = ml.stream()
        out_li = []
        for doc in docs:
            out_li.append(doc.to_dict())

    # /search?rating  -- Returns list of documents.
    elif 'rating' in args:
        rating = args.get('rating')

        # Firebase query.
        ml = doc_ref.where(u'restaurant_rating', u'>=', float(rating))
        docs = ml.stream()
        dummy = []

        for doc in docs:
            dummy.append(doc.to_dict())

        # Sorting the list by rating in descending order.
        out_li = sorted(dummy, key=lambda y: y['restaurant_rating'], reverse=True)

    # /search?price_type  -- Returns list of documents.
    elif 'price_type' in args:
        price = args.get('price_type')

        # Firebase query.
        ml = doc_ref.where(u'price_type', u'==', price)
        docs = ml.stream()
        dummy = []

        for doc in docs:
            dummy.append(doc.to_dict())

        # Sorting the list by name in ascending order.
        out_li = sorted(dummy, key=lambda y: y['restaurant_name'], reverse=False)

    # /search?latitude & longitude  -- Returns nearest restaurants within 5km radius.
    elif ('latitude' in args) and ('longitude' in args):
        lat = args.get('latitude')
        lon = args.get('longitude')

        # Use precision=5 to locate restaurants within 5km radius.
        search_geo = pgh.encode(float(lat), float(lon), precision=5)

        # Firebase query.
        ml = doc_ref.where(u'geohash', u'==', search_geo)
        docs = ml.stream()

        dummy = []
        ind = {}
        out_li = []

        for doc in docs:
            dummy.append(doc.to_dict())

        # Dictionary having distance in key and id in value.
        for idx, dummy_item in enumerate(dummy):
            key = distance.distance((lat,lon), (dummy_item['lat'], dummy_item['lon']))
            value = idx
            ind[key] = value

        # sorting the dictionary on keys (Distance).
        ind_sorted = sorted(ind.items())

        for z in ind_sorted:
            out_li.append(dummy[z[1]])

    else:
        return "Invalid Input"


    return jsonify(results = out_li)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)
