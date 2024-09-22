import random
import string
from django.conf import settings


class Shortener:
    # token_size = 5

    # def __init__(self, token_size=None):
    #     self.token_size = token_size  # if token_size is not specified else 5

    def generate_token(self):
        letters = string.ascii_letters
        # print(letters)
        # return ''.join([random.choice(letters) for i in range(self.token_size)])
        # for i in range(self.token_size)
        # print(range(10))
        # print()
        # return ''
        # print(''.join(random.choice(letters) for i in range(10)))
        return ''.join(random.choice(letters) for i in range(settings.SHORT_URL_TOKEN_SIZE))