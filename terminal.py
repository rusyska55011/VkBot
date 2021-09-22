import vk
from settings import VkSettings


class Vk:
    def __init__(self):
        self.vk_base = vk.VkBase()
        self.vk_bot = vk.VkBot(access_token=VkSettings.access_token)

    def start_chat_bot(self):
        vk.LongPool(self.vk_bot, VkSettings.chat_bot_asks).start()

    def start_friend_checker(self):
        vk.AddUsersChecker(self.vk_bot, VkSettings.message_for_added_users, self.vk_bot.get_friends_list()).start()

    def push(self, message: str=None):
        if not message:
            message = VkSettings.default_pushing_message
            print(f'Внимание! ТЫ не ввел текст сообщения! Будет запушено дефолтное значение:\n{message}\n')
        print(f'Для начала пуша введи Y, для отмены N')
        while True:
            start = str(input()).upper()
            if start == 'Y':
                self.vk_bot.push_messages(message)
                break
            elif start == 'N':
                print('Действие отменено')
                break
            else:
                print('Введи корректное значение')

    def add_by_id(self, *args: int):
        for vk_id in args:
            self.vk_bot.add_by_id(vk_id)

    def add(self, *args: list):
        self.vk_base.add(*args)

    def delete(self, *args: int):
        self.vk_base.delete(*args)

    def read(self):
        print(self.vk_base.get_col_names())
        for vk_id, name in self.vk_base.read():
            print(vk_id, '|', name)