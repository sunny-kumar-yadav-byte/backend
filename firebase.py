import firebase_admin
import json
import os
from firebase_admin import credentials, firestore

key = json.loads(os.environ["FIREBASE_KEY"])
cred = credentials.Certificate(key)

firebase_admin.initialize_app(cred)
db = firestore.client()
