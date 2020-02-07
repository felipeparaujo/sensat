from aumbry import Attr, YamlConfig


class DatabaseConfig(YamlConfig):
    __mapping__ = {
        'host': Attr('host', str),
        'db': Attr('db', str),
        'user': Attr('user', str),
        'password': Attr('password', str),
        'port': Attr('port', int),
    }

    host = ''
    db = ''
    user = ''
    password = ''
    port = 3306


class AppConfig(YamlConfig):
    __mapping__ = {
        'db': Attr('db', DatabaseConfig),
    }

    def __init__(self):
        self.db = DatabaseConfig()
