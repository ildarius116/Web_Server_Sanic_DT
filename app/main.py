from sanic import Sanic, response
from sanic.response import json, html
from sanic_jinja2 import Environment, PackageLoader
from sanic_auth import Auth, User as User_Auth
from sqlalchemy import select
from app.routes import user_bp, crud_bp, payment_bp
from app.database import async_session
from app.models import User
from app.routes.user_routes import add_user_routes
from app.routes.crud_routes import add_user_crud
from app.encrypting import check_password
import logging

logger = logging.Logger(__name__)

# Создаем окружение для шаблонов html страниц
env = Environment(loader=PackageLoader('app', 'templates'))
# Создаем приложение Sanic
app = Sanic('MyApp')
app.config.AUTH_LOGIN_ENDPOINT = 'login'

# Создаем аутентификацию
auth = Auth(app)

# Регистрируем Blueprints
app.blueprint(user_bp)
app.blueprint(crud_bp)
app.blueprint(payment_bp)

# Подключение прочих эндпоинтов с проброской аргументов (аутентификацию и окружение)
add_user_routes(auth, env)
add_user_crud(auth, env)

session = {}


@app.middleware('request')
async def add_session(request) -> None:
    """
    Функция доп обработки запроса - "request".
    Добавляет в запрос текущую сессию.

    :param request:
    :return: None
    """
    request.ctx.session = session
    logger.info(f"request.ctx.session: {request.ctx.session}")


@app.route('/')
@auth.login_required(user_keyword='user')
async def profile(request, user) -> html:
    """
    Функция добавляет корневой эндпоинт "/" (стартовая страница) всего приложения.

    :param request:
    :param user: Данные авторизации пользователя.
    :return: html: HTML Страница
    """
    logger.info(f"user: {user}")
    template = env.get_template('index.html')
    html_content = template.render(user=user)
    return html(html_content)


@app.route('/login', methods=['GET', 'POST'])
async def login(request) -> html:
    """
    Функция добавляет эндпоинт "/login" для авторизации пользователя..

    :param request: POST: email, password
    :return: html: HTML Страница
    """
    message = ''
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        logger.warning(f"email: {email}, password: {password}")
        async with async_session() as session:
            result = await session.execute(select(User).where(User.email == email))
            logger.warning(f"result: {result}")
            user = result.scalars().first()
            logger.warning(f"user: {user}")
        if user and check_password(password, user.password):
            logger.warning(f"email: {email}, password: {password}")
            user_auth = User_Auth(id=user.id, name=user.full_name)
            auth.login_user(request, user_auth)
            return response.redirect('/')
        message = 'invalid username or password'
    template = env.get_template('login.html')
    html_content = template.render(message=message)
    return html(html_content)


@app.route('/logout')
@auth.login_required
async def logout(request) -> html:
    """
    Функция добавляет эндпоинт "/logout" для выхода пользователя из системы.

    :param request:
    :return: html: HTML Страница
    """
    auth.logout_user(request)
    return response.redirect('/login')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
