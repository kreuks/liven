import json


with open('bot/config.json', 'r') as f:
    _config = json.load(f)

config = _config['config']
