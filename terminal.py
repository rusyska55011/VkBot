import os
import main


def start():
    os.startfile('main.py')

# Работает только если запущен main.py!!
def add_by_id(id):
    main.vk_bot.add_by_id(id)