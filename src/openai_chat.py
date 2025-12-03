from openai import AsyncOpenAI
from openai.types.responses import ResponseInputItemParam
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import OPENAI_API_KEY
import tiktoken
from src.storage import update_chat_history, get_chat_history, replace_chat_history

def num_tokens_from_messages(messages, model='gpt-5-nano'):
  """Returns the number of tokens used by a list of messages.
  Copied with minor changes from: https://platform.openai.com/docs/guides/chat/managing-tokens """
  try:
      encoding = tiktoken.encoding_for_model(model)
      num_tokens = 0
      for message in messages:
          num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
          for key, value in message.items():
              num_tokens += len(encoding.encode(value))
              if key == "name":  # if there's a name, the role is omitted
                  num_tokens += -1  # role is always required and always 1 token
      num_tokens += 2  # every reply is primed with <im_start>assistant
      print(num_tokens)
      return num_tokens
  except Exception:
      raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}.
      #See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")


class OpenAIManager:

    def __init__(self, instructions=""):
        self.ai_model = "gpt-5-nano"
        self.model_instructions=instructions
        try:
            self.client = AsyncOpenAI(api_key=OPENAI_API_KEY)
        except TypeError:
            exit("Wrong API Key")

    async def chat_no_history(self, prompt=""):

        if not prompt:
            print("No prompt passed in")
            return
        
        chat_question: list[ResponseInputItemParam] = [{"role": "user", "content": prompt}]
        if num_tokens_from_messages(chat_question) > 500:
            print("Prompt to large and I'm a cheap bitch and don't want to spend money")
            return

        response = await self.client.responses.create(
            model=self.ai_model,
            instructions=self.model_instructions,
            input=chat_question,
        )

        return response.output_text


    async def chat_with_history(self, prompt=""):
        if not prompt:
            print("No Prompt Passed in")
            return

        chat_question = {"role": "user", "content": prompt}

        chat_history = update_chat_history(chat_question)

        messagePopped = False
        while num_tokens_from_messages(chat_history) > 2500:
            chat_history.pop(1)
            messagePopped = True
            print("Popped Message!")

        #TODO: make the replace_chat_history into a remove message function that way I keep storage logic in one place
        if messagePopped:
            replace_chat_history(chat_history)
        
        print(chat_history)

        response = await self.client.responses.create(
                model=self.ai_model,
                instructions=self.model_instructions,
                input=chat_history,
        )

        update_chat_history({"role":"assistant", "content": response.output_text})

        return response.output_text







