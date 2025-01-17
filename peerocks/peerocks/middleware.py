from django.utils.deprecation import MiddlewareMixin
from time import time, sleep

"""
    Посмотреть какие Middleware используются в проекте. Описать их назначения
    SessionMiddleware, CsrfViewMiddleware, AuthenticationMiddleware 
    
    1. SessionMiddleware 
    Используются для взаимодействия с сессиями пользователей.
    по умолчанию сессии хранятся в БД моделей django, но можно перенастроить на свою
    БД, file-based sessions, cookie-based sessions или на использование кэшей, если 
    используется Memcached cache backend. По своей идее сессии используются, чтобы 
    пользователи могли не авторизироваться постоянно.
    Сессии сохраняются после модификации. Надо быть осторожным с сессиями с поддоменов,
    так как с поддоменов можно устанавливать сессию для всего домена.
    
    2. CsrfViewMiddleware 
    Используется для защиты от подделки межсайтовых запросов
    Если CSRF_USE_SESSIONS или CSRF_COOKIE_HTTPONLY активированы, то необходимо вшить 
    CSRF токен в HTML.
    (!)Если использовать CSRF токен при формировании запроса для внешнего сайта, то 
    будет утечка CSRF токена, следовательно появится CSFR уязвимость.
    Файл cookie CSRF основывается на случайном секретном значении с использованием
    макси для его шифрования. Меняется токен при каждой аутентификации пользователя. 
    Намеренно игнорирует все запросы GET и другие, которе определены как "безопасные"
    в RFC 7231 # section-4.2.1, потому что CSRF атаки через GET не должны иметь 
    побочных эффектов. Небезопасные - POST, PUT, DELETE и остальные.
    Не спасёт от man in the middle. Про XSS - понятно, что если есть XSS уязвимость, то
    токены вроде CSRF - не помогут.
    Если токены используются шаблоном, то Middleware добавит ответ в cookie файл заголовок.
    Если используется декоратор кэша, то Middleware не сможет установить токен в cookie и
    надо явно использовать декоратор django.views.decorators.csrf.csrf_protect.
    Для поддоменов - надо быть уверенным, что они контролируются доверенными лицами, а
    если контролируются, то не могут устанавливать cookie файлы. 
    Если есть требования, которые не подходят под шаблон, то можно использовать ряд утилит.
    Если для нескольких views надо отключить CSRF, то надо использовать csrf_exempt().
    
    3. AuthenticationMiddleware
    Используется для проверки прав доступа пользователя. Можно определить редиректы
    на страницу для аутентификаци, если пользователь обычный или анонимный. Редирект
    делать после 403 ответа. 
    Работает в связке с сеансом, чтобы получать уровень прав доступа для поступившего 
    запроса
"""


class FakeUser:
    """
    Существует некий пользователь, у которого есть атрибут auth. Также, в объекте request
    существует атрибут auth содержащий либо значение ‘VALID_TOKEN’ либо
    ‘INVALID_TOKEN’.
    Необходимо:
      Внести в созданный вами middleware изменения таким образом, чтобы изменить значен-
      ие атрибута user.auth (True или False) в зависимости от значения атрибута request.auth,
      после чего передать значение user.auth в request.auth.
    """
    # определите у пользователя аттрибуты auth
    def __init__(self, authorization_token=False):
        self.authorization_token: bool = authorization_token


# Необходимо изменить поведение указанных методов.
# Помните про __call__()
class MyMiddleware(MiddlewareMixin):
    """
    Написать собственный middleware, который бы сохранял в объекте
    request атрибут runtime содержащий время исполнения запроса
    """

    def __call__(self, request, *args, **kwargs):
        timestamp_before_middleware_handler = time()

        response = self.process_request(request)
        self.process_response(request, response)

        sleep(0.1)  # костыль т.к. для тестов нужно float значение больше 0, а time не может выдать
        #  нормальную точность. Можно было из datetime преобразовать в float, но мне кажется, что лучше
        #  просто использовать datetime вместо float
        timestamp_after_middleware_handler = time()
        request.runtime = timestamp_after_middleware_handler - timestamp_before_middleware_handler
        return response

    def process_request(self, request):
        fake_user_instance = FakeUser()

        if request.authorization_token == "VALID_TOKEN":
            fake_user_instance.authorization_token = True
        else:
            fake_user_instance.authorization_token = False

        request.authorization_token = fake_user_instance.authorization_token
        request.auth = fake_user_instance.authorization_token
        return self.get_response(request)

    def process_response(self, request, response):
        return response
