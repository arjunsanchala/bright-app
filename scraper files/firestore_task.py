
# Importing libraries.
import scraper
import firebase_admin
from firebase_admin import credentials, firestore

# Utilizing all the fuctions of the 'scraper.py' file.
def preprocessing():
    proxy = scraper.ListOfProxies()

    restaurant_list = scraper.MakeRestaurantList(proxy)

    restaurant_Details = scraper.AddingRestaurantDetails(restaurant_list)

    adding_more_features = scraper.AddingMoreFeatures(restaurant_Details, proxy)

    final_Document = scraper.AddingLocationFeatures(adding_more_features)

    return final_Document

# Function to upload the data to Firestore collection.
def UploadToFirestore(data):

    # Add you credentials below.
    cred = credentials.Certificate('./bright-pro-firebase-adminsdk-1ao7r-920e09b64c.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    # Uploading documents to the collection.
    doc_ref = db.collection(u'venues')
    list(map(lambda x: doc_ref.add(x), data))

    return "Data Uploaded successfully.."


Data_to_upload =preprocessing()
UploadToFirestore(Data_to_upload)