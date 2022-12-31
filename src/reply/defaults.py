from random import choice

from src.system.json import *
from database.directories import *


async def defaults(message):
    DEFAULTS = dict(read_json(DIR_DEFAULTS))
    KEYS = list(DEFAULTS.keys())

    for key in KEYS:
        for word in DEFAULTS[key]["var"]:
            word = word.lower()
            m = message.content.lower()

            if word in m:
                send = choice(DEFAULTS[key]["reply"])
                await message.channel.send(send)

                print(f"{send} | SEND |"); break
