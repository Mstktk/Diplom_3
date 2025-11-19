import os

class PersonalData:
    PASSWORD = os.getenv('USER_PASSWORD', '1602151')
    EMAIL = os.getenv('USER_EMAIL', 'mstktk@yandex.ru')
