import firebase_admin
from firebase_admin import credentials, firestore
import os
import json
import base64

firebase_creds_base64 = os.getenv("FIREBASE_CREDENTIALS_BASE64")

if firebase_creds_base64:
    decoded_creds_str = base64.b64decode(firebase_creds_base64).decode('utf-8')
    creds_dict = json.loads(decoded_creds_str)
    cred = credentials.Certificate(creds_dict)
else:
    print(f"AVISO: Variável de ambiente do Firebase não encontrada. Usando arquivo local.")
    cred_path = os.path.join(os.path.dirname(__file__), '..', 'firebase-credentials.json')
    cred = credentials.Certificate(cred_path)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()
config_doc_ref = db.collection('system_config').document('reaction_roles')

def get_reaction_config():
    doc = config_doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    return {}

def set_config_value(key: str, value):
    config_doc_ref.set({key: value}, merge=True)

def add_role_mapping(emoji: str, role_id: int):
    config_doc_ref.update({f'role_mappings.{emoji}': role_id})