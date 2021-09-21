from dotenv import dotenv_values

# vk
access_token, user_id = dotenv_values('.env').values()
message_for_added_users = 'Привет, +name+! Спасибо что добавился в друзья!'
