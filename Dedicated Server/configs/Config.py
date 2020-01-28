class DefaultConfig:
    DEBUG = False
    Admin = 'Name'
    Password = 'word'


class UserConfig(DefaultConfig):
    DEBUG = True
    SECRET_KEY = '1s1E4n5P1a4i1Y9a1J9y8U10'
