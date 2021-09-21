from dotenv import dotenv_values

# vk
access_token, user_id = dotenv_values('.env').values()
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
