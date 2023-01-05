import openai

from database.directories import *
from src.system.json import *


BOT = dict(
    read_json(DIR_SECRET["SYSTEM"])
)
openai.api_key = BOT["OPENAI_API_KEY"]

response = openai.Completion.create(
  model="text-davinci-003",
  prompt="Como fazer um bolo de cenoura?",
  temperature=0.6,
  max_tokens=150,
  top_p=1,
  frequency_penalty=1,
  presence_penalty=1
)

text = response["choices"][0]["text"]
text = "".join(text)

print(text)