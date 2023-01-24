import openai, requests
from pprint import pprint

from database.directories import *
from src.system.json import *


BOT = dict(
    read_json(DIR_SECRET["SYSTEM"])
)
openai.api_key = BOT["OPENAI_API_KEY"]

response = openai.Image.create(
  prompt="ate que durou",
  size="1024x1024", n=1
)
image_url = response['data'][0]['url']; pprint(response)
output = requests.get(image_url)

# open('assets/downloads/dall_e2.png', 'wb').write(output.content)
# OR ->

# file = open('assets/downloads/dall_e2.png', 'wb')
# file.write(output.content)
# OR ->

with open('assets/downloads/dall_e2.png', 'wb') as file:
  file.write(output.content)