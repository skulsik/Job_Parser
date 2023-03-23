from abc import abstractmethod


class Error(Exception):
    """ Глобальная переменная для отлова ошибок """
    NotError: str = None


class RequestError(Error):
    """
    Ошибка доступа к странице
    Возвращает переданную ошибку, либо предопределенную
    """
    def __init__(self, *args, **kwargs):
        # Словарь с ошибками
        error_dict: dict = {4: 'RequestError: Ошибка клиента.', 5: 'RequestError: Ошибка сервера.'}
        self.message: str = error_dict[int(args[0] / 100)] if args else 'RequestError: Неизвестная ошибка.'
        Error.NotError: str = self.message
        print(self.message)


class APIKeyError(Error):
    """
    Ошибка ключа в переменных окружения
    Возвращает переданную ошибку, либо предопределенную
    """
    def __init__(self, *args, **kwargs):
        self.message: str = args[0] if args else 'APIKeyError: Неизвестная ошибка.'
        Error.NotError: str = self.message
        print(self.message)


class HTTPError(Error):
    """
    Ошибка переданного адреса
    Возвращает переданную ошибку, либо предопределенную
    """
    def __init__(self, *args, **kwargs):
        self.message: str = args[0] if args else 'HTTPError: Неизвестная ошибка.'
        Error.NotError: str = self.message
        print(self.message)


class NameKeyError(Error):
    """
    Ошибка переданного имени
    Возвращает переданную ошибку, либо предопределенную
    """
    def __init__(self, *args, **kwargs):
        self.message: str = args[0] if args else 'NameKeyError: Неизвестная ошибка.'
        Error.NotError: str = self.message
        print(self.message)


class ListError(Error):
    """
    Ошибка переданного имени
    Возвращает переданную ошибку, либо предопределенную
    """
    def __init__(self, *args, **kwargs):
        self.message: str = args[0] if args else 'NameKeyError: Неизвестная ошибка.'
        Error.NotError: str = self.message
        print(self.message)
