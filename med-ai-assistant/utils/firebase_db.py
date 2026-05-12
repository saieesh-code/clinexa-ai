# Optional Firebase integration

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def initialize_firebase():

    cred = credentials.Certificate("firebase_key.json")

    firebase_admin.initialize_app(cred)

    db = firestore.client()

    return db