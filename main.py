from time import sleep
from random import randint
from threading import Thread


class AddUsersChecker:
    def __init__(self, vk_bot, message_for_added_users: str, friends_list: list):
        self.message_for_added_users = message_for_added_users
        self.friends_list = friends_list
        self.vk_bot = vk_bot

    def start(self):
        userschecker_thread = Thread(target=self.__process)
        userschecker_thread.start()

    def __process(self):
        while True:
            get_friends = self.vk_bot.get_friends_list()
            check = self.check_friends(self.friends_list, get_friends)

            if check:
                print('Обнаружены новые друзья! ID:', check)
                for vk_id in check:
                    self.vk_bot.send_message(vk_id, self.message_for_added_users)
                # Чтобы бот забывал друзей, которые удались из списка друзей,
                # можно передвинуть переменную за блок if
            self.friends_list = get_friends

            sleep(randint(5, 15))

    @staticmethod
    def check_friends(actual_friends_list: list, new_friends_list: list) -> list:
        if actual_friends_list != new_friends_list:
            new_friends = [item for item in new_friends_list if item not in actual_friends_list]
            return new_friends
        else:
            return []


class LongPool:
    def __init__(self, vk_bot, bot_asks: dict):
        self.bot_asks = bot_asks
        self.vk_bot = vk_bot

    def start(self):
        longpool_thread = Thread(target=self.vk_bot.start_longpoll, args=(self.bot_asks,))
        longpool_thread.start()
