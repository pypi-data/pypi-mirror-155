class ParsingAccount:
    """
    Абстрактный класс

    :param login: Логин аккаунта ВКонтакте (или любое другое описание аккаунта)
    :type login: str
    
    :param token: Токен аккаунта ВКонтакте
    :type token: str
    
    :param cooldown: Задержка между запросами к api
    :type cooldown: float
    
    :param logger: Логгер, определённый пользователем
    :type logger: logging.Logger
    """

    def __init__(self, login, token, cooldown, logger):
        self.login = login
        self.token = token
        self.cooldown = cooldown
        self.logger = logger
        self.can_single = False
        self.can_bucket = False

    def __hash__(self):
        return hash((self.login, self.token))

    def auth(self):
        """ Аутентификация аккаунта.

        Метод, вызывающийся для аккаунта один раз.
        Бросает исключение, если авторизация невозможна.
        """
        pass

    def check(self):
        """ Проверка аккаунта

        Метод, устанавливающий `can_single` и `can_bucket`
        Где
        `can_single` - может ли аккаунт выполнять единичные запросы 
        `can_bucket` - может ли аккаунт выполнять групповые запросы
        """
        pass

    def error_filter(self, error):
        """ Фильтр ошибок, бросаемых обращением к API

        :param error: Фильтруемая ошибка
        :type error: Exception

        Не бросает исключение, если после получения данной ошибки аккаунт нельзя использовать
        Бросает исключение, если ошибка не зависит от аккаунта, в том числе
            `StopParsingError`, если ошибка особо опасна
            Любое другое исключение, если ошибка относится к окружению (например `ApiHttpError`)
        """
        pass
 
    def method(self, method_name, method_args, callback, callback_args, callback_kwargs):
        """ Вызов метода API
        
        :param method: Название метода API
        :type method: str

        :param method_args: Параметры метода API
        :type method_args: dict
        
        :param callback: Вызываемый коллбэк по выполнении запроса
        :type callback: function

        :param callback_args: Аргументы коллбэка
        :type callback_args: tuple

        :param callback_kwargs: Именованые аргументы коллбэка
        :type callback_kwargs: dict

        Коллбэк вызывается следующим образом: callback(response, *callback_args, **callback_kwargs)
 
        Используя `error_filter`:
        Бросает `StopParsingError` в случае необходимости остановить парсинг.
        Бросает `BrokenAccountError` в случае необходимости остановить парсинг на этом аккаунте.
        Пробрасывает исключение в случае ошибки при вызове callback-а
        Пробрасывает исключение в случае ошибки окружения (например `ApiHttpError` и нестрашные ошибки API: `ApiError`)        

        Возвращает `response['response']` в случае успеха
        """
        pass
