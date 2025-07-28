import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("firebase_key.json")  # Baixe do console Firebase
firebase_admin.initialize_app(cred)
db = firestore.client()

def get_user(user_id):
    return db.collection("users").document(str(user_id))

def update_user(user_id, data):
    user_ref = get_user(user_id)
    user_ref.set(data, merge=True)