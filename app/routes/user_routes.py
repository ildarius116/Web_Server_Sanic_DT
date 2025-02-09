from sanic import Sanic, Blueprint
from sanic.response import html
from sanic.exceptions import NotFound
from sanic_auth import Auth
from sanic_jinja2 import Environment
from sqlalchemy import select
from app.models import User, Account, Payment
from app.database import async_session
import logging

logger = logging.Logger(__name__)

# Blueprint для маршрутов пользователей
user_bp = Blueprint("user_routes", url_prefix="/user")


def add_user_routes(auth: Auth, env: Environment):
    """
    Функция добавляет эндпоинты для перемещения пользователей по сайту.
    "/", "/<user_id:int>", "/<user_id:int>/accounts", "/<user_id:int>/accounts" с префиксом "/user"

    :param auth: авторизованный пользователь
    :param env: окружение
    """

    @user_bp.route('/', methods=['GET'])
    async def get_users(request) -> html:
        """
        Функция добавляет корневой эндпоинт "/" для получения списка всех пользователей.

        :param request:
        :return: html: HTML Страница
        """
        if auth.current_user(request):
            cur_user_id = auth.current_user(request).id
            async with async_session() as session:
                result = await async_session().execute(select(User).where(User.id == cur_user_id))
                user = result.scalars().first()
                if not user:
                    raise NotFound("User not found")
                logger.warning(f"user: {user}")
                if user.is_admin:
                    template = env.get_template('users-list.html')
                    async with async_session() as session:
                        result = await session.execute(select(User))
                        # result = await session.execute(select(User).where(User.is_admin == 0))
                        users = result.scalars().all()
                        html_content = template.render(users=users, user_id=cur_user_id)
                        return html(html_content)
                else:
                    html_content = env.get_template('forbidden.html').render()
                    return html(html_content)
        else:
            html_content = env.get_template('forbidden.html').render()
            return html(html_content)

    @user_bp.route('/<user_id:int>', methods=['GET'])
    async def get_user(request, user_id) -> html:
        """
        Функция добавляет эндпоинт "/<user_id:int>" для входа пользователя в Личный Кабинет.

        :param request:
        :param user_id: id пользователя из адресной строки
        :return: html: HTML Страница
        """
        if auth.current_user(request) and auth.current_user(request).id == user_id:
            async with async_session() as session:
                result = await session.execute(select(User).where(User.id == user_id))
                user = result.scalars().first()
                if not user:
                    raise NotFound("User not found")
                logger.warning(f"user: {user}")
                template = env.get_template('user-lk.html')
                html_content = template.render(user=user, is_admin=user.is_admin)
                return html(html_content)
        else:
            html_content = env.get_template('forbidden.html').render()
            return html(html_content)

    @user_bp.route('/<user_id:int>/accounts', methods=['GET'])
    async def get_user_accounts(request, user_id) -> html:
        """
        Функция добавляет эндпоинт "/<user_id:int>/accounts" для получения списка всех счетов пользователя.

        :param request:
        :param user_id: id пользователя из адресной строки
        :return: html: HTML Страница
        """
        if auth.current_user(request):
            cur_user_id = auth.current_user(request).id
            async with async_session() as session:
                result = await session.execute(select(User).where(User.id == cur_user_id))
                user = result.scalars().first()
                if not user:
                    raise NotFound("User not found")
                logger.warning(f"user: {user}")
                if user.is_admin or auth.current_user(request).id == user_id:
                    async with async_session() as session:
                        result = await session.execute(select(Account).where(Account.user_id == user_id))
                        accounts = result.scalars().all()
                        accounts_list = [{"id": acc.id, "balance": acc.balance} for acc in accounts]
                        logger.warning(f"accounts_list: {accounts_list}")
                        template = env.get_template('user-accounts.html')
                        html_content = template.render(
                            accounts_list=accounts_list,
                            user_id=user_id,
                            is_admin=user.is_admin,
                            admin_id=cur_user_id,
                        )
                        return html(html_content)
                else:
                    html_content = env.get_template('forbidden.html').render()
                    return html(html_content)
        else:
            html_content = env.get_template('forbidden.html').render()
            return html(html_content)

    @user_bp.route('/<user_id:int>/payments', methods=['GET'])
    async def get_user_payments(request, user_id) -> html:
        """
        Функция добавляет эндпоинт "/<user_id:int>/payments" для получения списка всех платежей пользователя.

        :param request:
        :param user_id: id пользователя из адресной строки
        :return: html: HTML Страница
        """
        if auth.current_user(request) and auth.current_user(request).id == user_id:
            async with async_session() as session:
                result = await session.execute(select(Payment).where(Payment.user_id == user_id))
                payments = result.scalars().all()
                payments_list = [{"id": pay.id, "transaction_id": pay.transaction_id, "amount": pay.amount} for pay in
                                 payments]
                logger.warning(f"payments_list: {payments_list}")
                template = env.get_template('user-payments.html')
                html_content = template.render(payments_list=payments_list, user_id=user_id)
                return html(html_content)
        else:
            html_content = env.get_template('forbidden.html').render()
            return html(html_content)
