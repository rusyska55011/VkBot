class VkSettings:
    access_token = 'токен'

    default_pushing_message = 'Привет, +name+! Ты попал под пуш сообщений!'
    message_for_added_users = 'Привет, +name+! Спасибо что добавился в друзья!'
    chat_bot_asks = {
        'привет': 'Доброго времени суток, +name+!',
        'здравствуйте': 'И вам тоже, +name+'
    }

    # Не трогать! Защита от дурака!
    new_dict = dict()
    for key, item in chat_bot_asks.items():
        new_dict[str(key).capitalize()] = item
    chat_bot_asks = new_dict
