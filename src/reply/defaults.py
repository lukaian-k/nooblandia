from src.system.json import *
from src.system.directories import *


async def defaults(message):
    DEFAULTS = dict(read_json(DIR_DEFAULTS))
    KEYS = list(DEFAULTS.keys())

    for word in KEYS:
        m = message.content.lower()

        if m.startswith(word.lower()):
            await message.channel.send(DEFAULTS[word])
            print(f"{DEFAULTS[word]} | SEND |")
