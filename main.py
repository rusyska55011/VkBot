from dotenv import dotenv_values
from .root import VkBot, VkBase


access_token, user_id = dotenv_values('.env').values()

