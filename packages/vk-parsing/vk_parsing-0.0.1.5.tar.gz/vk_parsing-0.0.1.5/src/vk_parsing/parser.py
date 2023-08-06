from .accounts.sync_account import VkApiAccount
from .task import ParsingTask
from .lconfig import *
from .exceptions import *
import logging.config

DEFAULT_SLEEP_TIME = 0.4
DEFAULT_BUCKET_SIZE = 25

def forward(response):
    return response

class Parser:
    """
    :param logins: Список логинов ВК (или других произвольных описаний)
    :type logins: list
    
    :param tokens: Список токенов ВК (той же длины)
    :type tokens: list

    :param account_class: Некоторая релизация ParsingAccount
    :type account_class: class
    
    :param sleep_time: Время ожидания между запросами
    :type sleep_time: float

    :param bucket_size_limit: Размер пакета запросов для групповых запросов
    :type bucket_size_limit: float

    :param logger: Логгер, определённый пользователем
    :type logger: logging.Logger

    :param need_logging: Нужно ли логгировать
    :type need_logging: bool

    Два принципа:
    1) Выбрасывание StopParsingError оставляет парсер в невалидном состоянии, ожидается, что работа не будет продолжена
    2) Отложенная задача может быть не выполнена. В том числе, если коллбэк бросает исключение, накрылся интернет или получено StopParsingError 
    """
    
    def __init__(self, logins, tokens, account_class = VkApiAccount, sleep_time = DEFAULT_SLEEP_TIME, bucket_size_limit = DEFAULT_BUCKET_SIZE, logger = None, need_logging = True):
        if not need_logging:
            logging.config.dictConfig(SILENT_CONFIG)
            self.logger = logging.getLogger(list(SILENT_CONFIG["loggers"].keys())[0])
        elif logger == None:
            logging.config.dictConfig(LOGGING_CONFIG)
            self.logger = logging.getLogger(list(LOGGING_CONFIG["loggers"].keys())[0]) 
        else:
            self.logger = logger
        self.logger.debug("Parser was created, logging enabled")
        self.bucket_size_limit = bucket_size_limit
        self.current_account_index = -1
        self.tasks = []
        self.accounts = []
        if bucket_size_limit > DEFAULT_BUCKET_SIZE:
            raise RuntimeError("Too large bucket_size_limit")
        if len(logins) != len(tokens):
            self.logger.error("Weird list lengths, aborting")
            raise RuntimeError("No match login-token: different lengths")
        for login, token in zip(logins, tokens):
            if (not isinstance(login, str)) or (not isinstance(token, str)):
                self.logger.error("Strings were expected, aborting")
                raise RuntimeError("Strings were expected")
        temp_accounts = []
        for login, token in zip(logins, tokens):
            temp_accounts.append(account_class(login, token, sleep_time, self.logger))
        for account in temp_accounts:
            try:
                account.auth()
                account.check()
                self.accounts.append(account)
            except Exception as ex:
                self.logger.warning(f"Account {account.login} auth[or the first request] missed with error: {str(ex)}")
    
    def _get_next_account(self, need_single = False, need_bucket = False):
        """ Выбор аккаунта с необходимыми параметрами

        Бросает `StopParsingError`, если таких аккаунтов нет
        """

        if len(self.accounts) == 0:
            self.logger.error("No more accounts in Parser, aborting")
            raise StopParsingError("No more accounts at all")
        for i in range(len(self.accounts)):
            self.current_account_index += 1
            self.current_account_index %= len(self.accounts)
            account = self._get_current_account()
            acceptable = True
            if (need_single and not account.can_single):
                acceptable = False
            if (need_bucket and not account.can_bucket):
                acceptable = False
            if (acceptable):
                return account
        self.logger.error(f'No more accounts with need_single={need_single}, need_bucket={need_bucket}')
        raise StopParsingError(f'No more accounts with need_single={need_single}, need_bucket={need_bucket}')

    def _get_current_account(self):
        """ Возвращает нынешний аккаунт
        
        Бросает `StopParsingError`, если аккаунтов нет
        """

        if len(self.accounts) == 0:
            self.logger.error("No more accounts in Parser, aborting")
            raise StopParsingError("No more accounts at all")
        return self.accounts[self.current_account_index]

    def _find_account_by_hash(self, hsh):
        """ Возвращает аккаунт по хэшу

        Бросает `RuntimeError`, если такого аккаунта нет
        """

        for account in self.accounts:
            if (hsh == hash(account)):
                return account
        raise RuntimeError("No such account.")

    def _drop_current_account(self):
        """ Удаляет нынешний аккаунт
        
        Бросает `StopParsingError`, если больше аккаунтов нет
        """

        self.logger.debug(f"Erasing {self._get_current_account().login}")
        self.accounts.pop(self.current_account_index)
        if len(self.accounts) == 0:
            self.logger.error("No more accounts in Parser, aborting")
            raise StopParsingError("No more accounts at all")
        self.current_account_index %= len(self.accounts)

    def direct_call(self, method, method_args = {}, callback = forward, callback_args=(), callback_kwargs={}):
        """ Прямой запрос к API с доступного аккаунта
        
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
        В случае если callback не передан, то данный метод пробрасывает response напрямую

        Бросает `StopParsingError`, если необходимо
        Бросает ошибки окружения, типа `ApiHttpError` и нестрашные ошибки API: `ApiError`
        Пробрасывает исключения из коллбэка

        В случае успеха возвращает результат коллбэка
        """

        while(True):
            current_account = self._get_next_account(need_single=True, need_bucket=(True if (method == "execute") else False))
            try:
                return current_account.method(method, method_args, callback, callback_args, callback_kwargs)
            except BrokenAccountError as ex:
                self._drop_current_account() # Could raise StopParsingError
                continue

    def add_task(self, method, method_args, callback, callback_args=(), callback_kwargs={}):
        """ Отложенный запрос к API с доступного аккаунта
        
        Сигнатура аналогична сигнатуре метода `direct_call`.
    
        Исполняет execute_tasks, если достигнут `bucket_size_limit`
        Бросает ошибки аналогично методу execute_tasks
        """

        self.tasks += [ParsingTask(method, method_args, callback, callback_args, callback_kwargs)]
        if (len(self.tasks) > self.bucket_size_limit):
            raise StopParsingError("Bucket was somehow overloaded")
        if (len(self.tasks) == self.bucket_size_limit):
            self.execute_tasks()         

    def execute_tasks(self):
        """ Выполняет все существующие задачи
 
        Бросает `StopParsingError`, если необходимо
        Бросает ошибки окружения, типа `ApiHttpError` и нестрашные ошибки API: `ApiError`
        Пробрасывает исключения из коллбэка
        """
        while (len(self.tasks) > 0):
            self._execute_tasks()

    def _execute_tasks(self):
        """ Выполняет существующие задачи
       
        Может не исполнить все задачи, но в таком случае количество аккаунтов будет уменьшено 
        
        Бросает `StopParsingError`, если необходимо
        Бросает ошибки окружения, типа `ApiHttpError` и нестрашные ошибки API: `ApiError`
        Пробрасывает исключения из коллбэков
        """

        if (len(self.tasks) == 0):
            return
        code = "return ["
        for task in self.tasks:
            code += "API." + task.method + "(" + str(task.method_args) + "), " 
        code = code[:-2]
        code += "];"
        try:
            correct = self.direct_call("execute",
                        {"code": code},
                        self._execute_callbacks,
            )
        except Exception as ex:
            self.logger.error(f"Batch direct_call failed, cause: {ex}")
            self.tasks = []
            raise

        if not correct:
            self.logger.debug(f"Trying to understand if account needs mark can_backet=False with direct_calls")
            need_make_impotent = False
            hsh = hash(self._get_current_account())
            while self.tasks:
                task = self.tasks[0]
                self.tasks.pop(0)
                try:
                    self.direct_call(task.method, task.method_args, task.callback, task.callback_args, task.callback_kwargs)
                    need_make_impotent = True
                    break
                except ApiError as ex: # Задача никогда не сможет быть исполнена -- основной случай
                    pass
                except StopParsingError as ex: # Что-то пошло не так
                    self.logger.error(f"Callback threw exception, raising, cause: {ex}")
                    raise
                except ApiHttpError as ex: # Что-то не то с окружением
                    self.logger.error(f"Check direct_call failed, raising, cause: {ex}")
                    self.tasks = []
                    raise 
                except Exception as ex: # Коллбэк бросил исключение
                    self.logger.error(f"Callback threw exception, raising, cause: {ex}")
                    self.tasks = []
                    raise
            if need_make_impotent:
                self.logger.debug("Result: can_bucket=False")
                try:
                    self._find_account_by_hash(hsh).can_bucket = False
                except Exception as ex:
                    self.logger.debug(f"Strange error in execute_tasks: {ex}")
            else:
                self.logger.debug("Result: can_bucket=True")
        else:
            self.tasks = []

    def _execute_callbacks(self, response):
        """ Коллбэк, исполняющий коллбэки tasks
        
        В общем случае имеет право не исполнить некоторый коллбэк.
        Пробрасывает исключение и не выполняет следующие коллбэки, если один коллбэк бросает исключение.
        
        В случае отсутствия исключений
        Возвращает True, если получил хотя бы один ответ (бывают и пропуски, которые на деле False) в групповом ответе.
        Возвращает False иначе. На основе этого делается проверка по запросам в execute_tasks с помощью direct_call.
        """

        size = len(self.tasks)
        for i in range(len(self.tasks)):
            if (isinstance(response[i], bool) and not response[i]):
                size -= 1
        if (size == 0):
            self.logger.debug("Whole bucket request failed (response[i] = False)") 
            return False

        for i in range(len(self.tasks)):
            if (isinstance(response[i], bool) and not response[i]):
                continue
            self.tasks[i].callback(response[i], *self.tasks[i].callback_args, **self.tasks[i].callback_kwargs)
        return True
