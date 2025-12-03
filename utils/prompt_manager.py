from src.storage import get_scores, get_chat_history
from utils.formatting import scores_to_string

async def generate_prompt_chat(bot, message=""):
    generatedPrompt =  ""   

    if message == "":
        print("No prompt Passed in")
        return
    
    #for prompt it needs: scoreboard, message history

    scores = get_scores()

    scoresString = await scores_to_string(bot, scores)

    print(scoresString)

    chat_history = get_chat_history() 

    print(chat_history)
    
    #combine scoreboard string and chat_history 

    generatedPrompt = scoresString + chat_history 

    return generatedPrompt
     
