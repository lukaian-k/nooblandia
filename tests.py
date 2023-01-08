import os


for filename in os.listdir('src/cogs'):
  if filename == '__pycache__':
    continue
  print(filename)
  