import re

NEGATIVE_WORDS = {
    "fuck": -1, 
    "shit": -1,
    "bad": -1,
    "hate": -1,
    "stupid": -1,
    "idiot": -1,
    "dumb": -1,
    "terrible": -1,
    "lame": -1,
    "noob": -1,
    "loser": -1,
    "fail": -1,
    "bruh": -1,
    "ugh": -1,
    "annoying": -1,
    "mean": -1,
    "gross": -1,
    "ugly": -1,
    "sucks": -1,
    "trash": -1,
    "sad": -1,
    "angry": -1,
    "wtf": -1,
    "worthless": -1,
    "fool": -1,
    "mad": -1,
    "nasty": -1,
    "pog": -5,
}

YAPPING_STATUS = [15, 0, -5]

POSITIVE_PHRASES = {
        tuple(["ross", "fat"]): 10,
        tuple(["clay", "fat"]): 10             
}

POSITIVE_WORDS = {  
    "good":1,
    "great":1,
    "nice":1,
    "awesome":1,
    "fantastic":1,
    "amazing":1,
    "yay":1,
    "lol":1,
    "thanks":1,
    "thank you":1,
    "ok":1,
    "wp":1,
    "well played":1,
    "congrats":1,
    "congratulations":1,
    "bravo":1,
    "cool":1,
    "friendly":1,
    "happy":1,
    "love":1,
    "glad":1,
    "fun":1,
    "cheers":1,
    "excellent":1,
    "good job":1,
    "nice job":1,
    "well done":1,
    "sweet":1,
    "wow":1,
    "haha":1,
}

def positive_score(message) -> int: 
    score = 0

    content = message.lower()
    content_words = re.findall(r'\b\w+\b', content)

    #Identify Yapping status
    if len(content_words) < YAPPING_STATUS[0]:
        score += YAPPING_STATUS[1]
    
    #Positive Word Scoring
    for word, weight in POSITIVE_WORDS.items():
        count = content_words.count(word)
        score += weight * count


    #Positive Phrase Scoring
    for phrase, weight in POSITIVE_PHRASES.items():
        count = 0 
        for word in phrase:
            if word in content:
                count += 1

        if count == len(phrase):
            score += weight

    return score

def negative_score(message) -> int:
    score = 0

    content = message.lower()
    content_words = re.findall(r'\b\w+\b', content)

    #Identify Yapping Status
    if len(content_words) >= YAPPING_STATUS[0]:
        score += YAPPING_STATUS[2]
    
    #Negative Word Scoring
    for word, weight in NEGATIVE_WORDS.items():
        count = content_words.count(word)  # number of times the word appears
        score += weight * count    

    return score

def apply_rules(message) -> int:
    positive_change, negative_change = positive_score(message), negative_score(message)
    print(positive_change, negative_change)
    return positive_change + negative_change
