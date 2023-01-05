from random import choice, randint

from src.system.json import *
from database.directories import *


async def defaults(message):
    DEFAULTS = dict(read_json(DIR_DEFAULTS))
    KEYS = list(DEFAULTS.keys())

    for key in KEYS:
        for word in DEFAULTS[key]["var"]:
            word = word.lower()
            msg = message.content.lower()

            permission = randint(0,10)
            APPROVED = 1

            if word in msg and permission == APPROVED:
                send = choice(DEFAULTS[key]["reply"])
                await message.channel.send(send)

                print(f"{send} | SEND |"); return