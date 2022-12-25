import threading

import discord
import json

from googlesearch import search
import random
from numpy import number


app = {
    "client": "app/client.py",
    "bot": "app/bot.py",
}


def run_file(filename):
    exec(open(filename).read())

for i in app:
    print(f'Inicializando: {i}')

    if i == "client":
        continue
    run = threading.Thread(target=run_file, args=(app[i],))
    run.start()

print('\nInicialização completa!')

exec(open(app["client"]).read())
