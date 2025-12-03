from src.openai_chat import OpenAIManager

def main():
    model_instructions = "You are a coding assistant that talks like a pirate."
    ai = OpenAIManager(instructions=model_instructions)
    prompt = "Say hello in a funny way."
    response = ai.chat_with_history(prompt)
    print("AI Response:", response)

if __name__ == "__main__":
    main()
