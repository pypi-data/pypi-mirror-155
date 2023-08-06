from typing import BinaryIO

import requests
import json

from datetime import datetime

from jproperties import Properties

from elma.exceptions import ElmaApiException
from elma.models.auth_result import AuthResult
from elma.models.data.data import Data
from elma.models.data.data_implementations import StartProcess

AUTH_PATH = "/API/REST/Authorization/LoginWith?username={}"
START_PROCESS_PATH = "/API/REST/Workflow/StartProcess"
STARTABLE_PROCESSES_PATH = "/API/REST/Workflow/StartableProcesses"
API_VERSION_PATH = "/API/REST/Authorization/ApiVersion"
CONTENT_TYPE_HEADER = "Content-Type"
APPLICATION_JSON = "application/json; charset=utf-8"


class ElmaApiWebClient:
    __AuthTokenMaxMinutesAlive = 15
    __UserLogin: str
    __UserPassword: str
    __AuthToken: str
    __AuthTokenLiveTimestamp: float
    __SessionToken: str
    __AppToken: str

    def __init__(self, host_name: str, port: int, debug_mode=False) -> None:
        super().__init__()
        self.port = port
        self.host_name = host_name
        self.debug_mode = debug_mode

    # Создание инстанса веб-клиента с автоматической авторизацией запросов
    @staticmethod
    def init_with_auth(host_name: str, port: int, debug_mode=False,
                       user_login: str = None, user_password: str = None, app_token: str = None):
        instance = ElmaApiWebClient(host_name=host_name, port=port, debug_mode=debug_mode)
        auth_result = instance.auth(user_login=user_login, user_password=user_password, app_token=app_token)
        instance.__AuthToken = auth_result.AuthToken
        instance.__SessionToken = auth_result.SessionToken
        instance.__AppToken = app_token
        instance.__UserLogin = user_login
        instance.__UserPassword = user_password
        return instance

    # Создание инстанса веб-клиента с автоматической авторизацией запросов через конфигурационный файл .properties
    # *заполнять только один из аргументов*
    @staticmethod
    def init_with_auth_from_properties(config_file: BinaryIO, properties: dict = None):
        if properties is None:
            properties = {}
            path: str
            # if config_file_absolute_path is None:
            #     from pathology.path import Path
            #     dir = Path
            #     path = f'{dir}/{config_file_name}'
            # else:
            #     path = config_file_absolute_path
            configs = Properties()
            # with open(path, 'rb') as config_file:
            configs.load(config_file)
            for prop in configs.items():
                properties[prop[0]] = prop[1].data

        return ElmaApiWebClient.init_with_auth(
            host_name=properties["host"],
            port=properties["port"],
            debug_mode=properties.get("debug_mode", False),
            user_login=properties["user_login"],
            user_password=properties["user_password"],
            app_token=properties["application_token"]
        )

    # Получить токен из кэша. Если токен уже просрочен, то получить новый и закэшировать
    def get_cached_auth_token(self):
        date_now = datetime.now()
        date_of_token_creation = datetime.fromtimestamp(self.__AuthTokenLiveTimestamp)
        tdelta = date_now - date_of_token_creation
        max_minutes_alive = (self.__AuthTokenMaxMinutesAlive - 1) * 60
        if tdelta.seconds >= max_minutes_alive:
            auth_result = self.auth(user_login=self.__UserLogin,
                                    user_password=self.__UserPassword,
                                    app_token=self.__AppToken)
            self.__AuthToken = auth_result.AuthToken
        return self.__AuthToken

    # базовый запрос в elma
    def base_request(self, path="", headers=None, body=None, request_func=lambda u, h, b: requests.post(u, h, b)):
        if headers is None:
            headers = {}
        if body is None:
            body = {}
        headers[CONTENT_TYPE_HEADER] = APPLICATION_JSON
        url = f"{self.host_name}:{self.port}{path}"
        if self.debug_mode:
            print("\n")
            print(f"request url: {url}")
            print(f"request headers: {headers}")
            print(f"request body: {body}")
        r = request_func(url, headers, body)
        if self.debug_mode:
            print(f"response code: {r.status_code}")
            print(f"response status: {r.reason}")
            print(f"response body: {r.text}")
        if len(r.text) == 0 or r.status_code > 300:
            raise ElmaApiException(f"code: {r.status_code}; status: {r.reason}; content: {r.text}")
        return json.loads(r.text)

    # POST-запрос в elma
    def base_post_request(self, path: str = "", headers=None, body=None) -> dict:
        return self.base_request(path, headers, body,
                                 lambda u, h, b: requests.post(url=u, headers=h, data=b))

    # GET-запрос в elma
    def base_get_request(self, path: str = "", headers=None) -> dict:
        return self.base_request(path, headers, {},
                                 lambda u, h, b: requests.get(url=u, headers=h))

    # POST-запрос в elma с авторизацией
    def authorized_post_request(self, path: str = None, headers=None, body=None,
                                auth_token=None, session_token=None) -> dict:
        if headers is None:
            headers = {}
        cached_auth_token = self.get_cached_auth_token()
        if auth_token is None and cached_auth_token is not None:
            auth_token = cached_auth_token
        elif auth_token is not None:
            self.__AuthToken = auth_token
        else:
            raise ElmaApiException("auth_token is missing")

        if session_token is None and self.__SessionToken is not None:
            session_token = self.__SessionToken
        elif session_token is not None:
            self.__SessionToken = session_token

        headers["AuthToken"] = auth_token
        if session_token is not None:
            headers["SessionToken"] = session_token
        return self.base_post_request(path=path, headers=headers, body=body)

    # метод авторизации
    def auth(self, user_login: str = None, user_password: str = None, app_token: str = None) -> AuthResult:
        path = AUTH_PATH.format(user_login)
        headers = {
            "ApplicationToken": app_token
        }
        if self.__dict__.keys().__contains__("__SessionToken") and self.__SessionToken is not None:
            headers["SessionToken"] = self.__SessionToken
        body = f'"{user_password}"'
        json_dict = self.base_post_request(path=path, headers=headers, body=body)
        self.__AuthTokenLiveTimestamp = datetime.timestamp(datetime.now())
        return AuthResult(json_dict)

    # метод запуска процесса
    def start_process(self, context_vars: Data = Data(), process_name=None,
                      process_token: str = None, process_header_id: int = None,
                      auth_token: str = None, session_token: str = None) -> Data:

        body = StartProcess(context_vars=context_vars, process_name=process_name,
                            process_token=process_token, process_header_id=process_header_id).to_Data()
        json_result = self.authorized_post_request(path=START_PROCESS_PATH, headers={}, body=str(body),
                                                   auth_token=auth_token, session_token=session_token)
        return Data.from_json(json_result)

    # получить все запущенные процессы
    def get_startable_processes(self, auth_token: str = None, session_token: str = None) -> Data:
        json_result = self.authorized_post_request(path=STARTABLE_PROCESSES_PATH, headers={},
                                                   auth_token=auth_token, session_token=session_token)
        return Data.from_json(json_result)

    # получить версию API
    def api_version(self) -> dict:
        return self.base_get_request(path=API_VERSION_PATH)
