# profile_system.py

import firebase_admin
from firebase_admin import credentials, firestore
import os
from firebase_admin.firestore import Query
import json
import base64


firebase_creds_base64 = os.getenv("FIREBASE_CREDENTIALS_BASE64")

if firebase_creds_base64:
    decoded_creds_str = base64.b64decode(firebase_creds_base64).decode('utf-8')
    creds_dict = json.loads(decoded_creds_str)

    cred = credentials.Certificate(creds_dict)
else:
    # Plano B: Se a variável não estiver definida (para testes locais), usa o arquivo
    print("AVISO: Variável FIREBASE_CREDENTIALS_BASE64 não encontrada. Usando arquivo local firebase-credentials.json.")
    cred = credentials.Certificate("firebase-credentials.json")

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()
users_ref = db.collection('users')


def calculate_xp_for_next_level(level):
    return 5 * (level ** 2) + 50 * level + 100

def get_user_data(user_id):
    user_doc = users_ref.document(str(user_id)).get()
    if user_doc.exists:
        user_data = user_doc.to_dict()
        if 'badges' not in user_data:
            user_data['badges'] = []
        return user_data
    else:
        default_profile = {
            'level': 1,
            'xp': 0,
            'badges': [],
            'username': author.name,
            'avatar_hash': author.display_avatar.key 
        }
        users_ref.document(str(user_id)).set(default_profile)
        return default_profile

def update_user_xp(author: discord.User):
    user_id_str = str(author.id)
    user_data = get_user_data(author)

    user_data['xp'] += 15 

    xp_needed = calculate_xp_for_next_level(user_data['level'])
    leveled_up = False

    if user_data['xp'] >= xp_needed:
        user_data['level'] += 1
        user_data['xp'] -= xp_needed 
        leveled_up = True
        print(f"[⬆️] Usuário {user_id_str} subiu para o nível {user_data['level']}!")

    update_data = {
        'level': user_data['level'],
        'xp': user_data['xp'],
        'username': author.name,
        'avatar_hash': author.display_avatar.key
    }
    users_ref.document(user_id_str).update(update_data)
    
    user_data.update(update_data)
    return leveled_up, user_data


def get_leaderboard(limit=10):
    print(f"[🔄️] Buscando o top {limit} do leaderboard no Firestore...")
    
    query = users_ref.order_by(
        "level", direction=Query.DESCENDING
    ).order_by(
        "xp", direction=Query.DESCENDING
    ).limit(limit)

    docs = query.stream()

    leaderboard_data = []
    for doc in docs:
        user_data = doc.to_dict()
        user_data['id'] = doc.id  
        leaderboard_data.append(user_data)
        
    print(f" -> Encontrados {len(leaderboard_data)} usuários.")
    return leaderboard_data



def add_badge_to_user(user_id, badge_id):

    user_id_str = str(user_id)
    user_data = get_user_data(user_id_str)
    
    if badge_id in user_data['badges']:
        return False  
    
    users_ref.document(user_id_str).update({
        "badges": firestore.ArrayUnion([badge_id])
    })
    return True

interaction_counters_ref = db.collection('interaction_counters')


# interação
def increment_interaction_counters(author_id, member_id, interaction_type):
    author_id_str = str(author_id)
    member_id_str = str(member_id)

    author_doc_ref = interaction_counters_ref.document(f"{author_id_str}_{interaction_type}")
    author_doc_ref.set({'deu': firestore.Increment(1)}, merge=True)

    member_doc_ref = interaction_counters_ref.document(f"{member_id_str}_{interaction_type}")
    member_doc_ref.set({'recebeu': firestore.Increment(1)}, merge=True)

    author_count_new = author_doc_ref.get().to_dict().get('deu', 1)
    member_count_new = member_doc_ref.get().to_dict().get('recebeu', 1)

    return author_count_new, member_count_new
