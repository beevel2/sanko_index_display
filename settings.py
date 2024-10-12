from os import environ
import json


bot_token = environ.get('BOT_TOKEN')

admin_list = json.loads(environ.get('ADMIN_LIST'))
