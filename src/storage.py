import json
from config import SOCIAL_CREDIT_START
from utils.formatting import scores_to_string

SCORES_PATH = "data/scores.json"
CHAT_PATH = "data/chat_history.json"

def load_json(filename):
    with open(filename, "r") as f:
        data = json.load(f)

    return data 

def save_json(filename, data) -> bool:
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
            return True

    except Exception as e:
        print(e)
        return False


#User Management

def add_user(user_id, user_name, default_score) -> bool:
    scores = load_json(SCORES_PATH)  

    if str(user_id) in scores:
        print("User Already Exists In Scores")
        return False

    scores[str(user_id)] = { "name": user_name, "score": default_score}

    if save_json(SCORES_PATH, scores):
        print("User Added Successfully")
        return True       
    else:
        print("ERROR: Adding User Failed")
        return False


def get_user_score(user_id, user_name) -> int:
    scores = load_json(SCORES_PATH)

    if str(user_id) not in scores:
        add_user(user_id, user_name, SOCIAL_CREDIT_START) 
        return SOCIAL_CREDIT_START

    return scores[str(user_id)]["score"]


#This function makes no fucking sense in the context in which the data is formatted in other places I don't think it really matters in this case tho
def get_users_score(user_ids) -> list:
    scores = load_json(SCORES_PATH)

    user_scores = []
    for uid in user_ids:
        uid_str = str(uid)

        # If a user is missing from the JSON, default to 0
        score = scores.get(uid_str, {"score": 0})["score"]

        user_scores.append([uid_str, score])

    return user_scores


def update_user_score(user_id, new_score):
    scores = load_json(SCORES_PATH)
    chat_history = load_json(CHAT_PATH)

    scores[str(user_id)]["score"] = new_score
    
    chat_history[0] = {"role": "developer", "content": scores_to_string(scores)}

    save_json(SCORES_PATH, scores)
    save_json(CHAT_PATH, chat_history)

    print(f"Updated score to {scores[str(user_id)]['score']}")


def get_scores():
    scores = load_json(SCORES_PATH)
    return scores

def get_highest_and_lowest():
    scores = load_json(SCORES_PATH)

    max_user_id = max(scores, key=lambda uid: scores[uid]['score'])
    min_user_id = min(scores, key=lambda uid: scores[uid]['score'])

    max_user = (scores[max_user_id]['name'], scores[max_user_id]['score'])
    min_user = (scores[min_user_id]['name'], scores[min_user_id]['score'])

    return min_user, max_user


# Chat Hisotry Storage Management

def get_chat_history():
    chat_history = load_json(CHAT_PATH)
    
    return chat_history

def update_chat_history(newMessage):
    chat_history = get_chat_history()

    chat_history.append(newMessage)

    save_json(CHAT_PATH, chat_history)

    return chat_history

def replace_chat_history(newChatHistory):
    save_json(CHAT_PATH, newChatHistory)
    return



