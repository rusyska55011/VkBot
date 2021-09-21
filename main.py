from time import sleep
from random import randint
from dotenv import dotenv_values
from root import VkBot, VkBase


class AddUsersChecker:
    def __init__(self, message_for_added_users: str, friends_list: list):
        self.message_for_added_users = message_for_added_users
        self.friends_list = friends_list

    def start(self):
        while True:
            get_friends = vk_bot.get_friends_list()
            check = self.check_friends(self.friends_list, get_friends)

            if check:
                print('Обнаружен новые друзья! ID:', check)
                for vk_id in check:
                    vk_bot.send_message(vk_id, self.message_for_added_users)
                # Чтобы бот забывал друзей, которые удались из списка друзей,
                # можно передвинуть переменную за блок if
                self.friends_list = get_friends

            sleep(randint(50, 150))

    @staticmethod
    def check_friends(actual_friends_list: list, new_friends_list: list) -> list:
        if actual_friends_list != new_friends_list:
            new_friends = [item for item in new_friends_list if item not in actual_friends_list]
            return new_friends
        else:
            return []


access_token, user_id = dotenv_values('.env').values()
vk_bot = VkBot(access_token=access_token, user_id=user_id)
vk_base = VkBase()

AddUsersChecker('Привет, +name+! Спасибо что добавился в друзья!', vk_bot.get_friends_list()).start()


