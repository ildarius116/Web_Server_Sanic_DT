from sanic import Blueprint
from sanic.response import html
from sanic.exceptions import NotFound, HTTPException
from sanic_auth import Auth
from sanic_jinja2 import Environment
from sqlalchemy import select, update, delete
from app.models import User
from app.database import async_session
from app.encrypting import hash_password
import logging

logger = logging.Logger(__name__)

# Blueprint для маршрутов администрирования пользователей (CRUD)
crud_bp = Blueprint("crud_routes", url_prefix="/user/crud")


def add_user_crud(auth: Auth, env: Environment) -> None:
    """
    Функция добавляет эндпоинты для администрирования пользователей (CRUD).
    "/create", "/update", "/delete" с префиксом "/user/crud"

    :param auth: авторизованный пользователь
    :param env: окружение
    """

    @crud_bp.route('/create', methods=['GET', 'POST'])
    async def create_user(request) -> html:
        """
        Функция добавляет эндпоинт "/create" для создания пользователей.

        :param request:  POST: email, full_name, password, is_admin
        :return: html: HTML Страница
        """
        result_message = ""
        if auth.current_user(request):
            cur_user_id = auth.current_user(request).id
            async with async_session() as session:
                result = await session.execute(select(User).where(User.id == cur_user_id))
                user = result.scalars().first()
                if not user:
                    raise NotFound("User not found")
                logger.warning(f"user: {user}")
                if user.is_admin:
                    if request.method == 'POST':
                        email = request.form.get('email')
                        full_name = request.form.get('full_name')
                        password = request.form.get('password')
                        is_admin = request.form.get('is_admin')
                        if is_admin:
                            is_admin = 1
                        else:
                            is_admin = 0
                        logger.warning(f"got user data: "
                                       f"email: {email}, "
                                       f"full_name: {full_name}, "
                                       f"password: {password}, "
                                       f"is_admin: {is_admin}"
                                       )
                        try:
                            user = User(email=email,
                                        full_name=full_name,
                                        password=hash_password(password),
                                        is_admin=is_admin,
                                        )
                            session.add(user)
                            logger.warning(f"new_user_result: {user}")
                            await session.commit()
                            result = await session.execute(select(User).where(User.email == email))
                            user = result.scalars().first()
                            result_message = f"""Создан пользователь:
                                                   <b>id:</b> {user.id}
                                                   <b>email:</b> {user.email}
                                                   <b>ФИО:</b> {user.full_name}
                                                   <b>Пароль:</b> {user.password}
                                                   <b>Статус:</b> {("Пользователь", "Админ")[user.is_admin]}"""
                        except Exception as e:
                            result_message = f"""Ошибка создания пользователя: \n
                                                {e.args}"""
                            logger.warning(f"Ошибка создания пользователя: {e.args}")
                    template = env.get_template('user-create.html')
                    html_content = template.render(user_id=cur_user_id, result_message=result_message)
                    return html(html_content)
                else:
                    html_content = env.get_template('forbidden.html').render()
                    return html(html_content)
        else:
            html_content = env.get_template('forbidden.html').render()
            return html(html_content)

    @crud_bp.route('/update', methods=['GET', 'POST'])
    async def update_user(request) -> html:
        """
        Функция добавляет эндпоинт "/update" для обновления пользователей.

        :param request:  POST: id, email, full_name, password, is_admin
        :return: html: HTML Страница
        """
        result_message = ""
        if auth.current_user(request):
            cur_user_id = auth.current_user(request).id
            async with async_session() as session:
                result = await session.execute(select(User).where(User.id == cur_user_id))
                user = result.scalars().first()
                if not user:
                    raise NotFound("User not found")
                logger.warning(f"user: {user}")
                if user.is_admin:
                    if request.method == 'POST':
                        id = int(request.form.get('user_id'))
                        email = request.form.get('email')
                        full_name = request.form.get('full_name')
                        password = request.form.get('password')
                        is_admin = request.form.get('is_admin')
                        new_data = {}
                        if email:
                            new_data["email"] = email
                        if full_name:
                            new_data["full_name"] = full_name
                        if password:
                            new_data["password"] = hash_password(password)
                        if is_admin:
                            new_data["is_admin"] = 1
                        else:
                            new_data["is_admin"] = 0
                        logger.warning(f"got user data: {new_data.items()}")
                        try:
                            result = await session.execute(select(User).where(User.id == id))
                            user_to_update = result.scalars().first()
                            if not user_to_update:
                                raise HTTPException(f"Пользователь c id({id}) не найден")
                            result = await session.execute(update(User).where(User.id == id).values(**new_data))
                            await session.commit()
                            logger.warning(f"Результат обновления пользователя: {result}")
                            result_message = f"""Обновлен пользователь:
                                                   <b>id:</b> {user_to_update.id}
                                                   <b>email:</b> {user_to_update.email}
                                                   <b>ФИО:</b> {user_to_update.full_name}
                                                   <b>Пароль:</b> {user_to_update.password}
                                                   <b>Статус:</b> {("Пользователь", "Админ")[user_to_update.is_admin]}
                                                """
                        except Exception as e:
                            result_message = f"""Ошибка обновления пользователя: 
                                                {e.args}"""
                            logger.warning(f"Ошибка обновления пользователя: {e.args}")
                    template = env.get_template('user-update.html')
                    html_content = template.render(user_id=cur_user_id, result_message=result_message)
                    return html(html_content)
                else:
                    html_content = env.get_template('forbidden.html').render()
                    return html(html_content)
        else:
            html_content = env.get_template('forbidden.html').render()
            return html(html_content)

    @crud_bp.route('/delete', methods=['GET', 'POST'])
    async def delete_user(request) -> html:
        """
        Функция добавляет эндпоинт "/delete" для удаления пользователей.

        :param request:  POST: id
        :return: html: HTML Страница
        """
        result_message = ""
        if auth.current_user(request):
            cur_user_id = auth.current_user(request).id
            async with async_session() as session:
                result = await session.execute(select(User).where(User.id == cur_user_id))
                user = result.scalars().first()
                if not user:
                    raise NotFound("User not found")
                logger.warning(f"user: {user}")
                if user.is_admin:
                    if request.method == 'POST':
                        id = int(request.form.get('user_id'))
                        logger.warning(f"got user_id to delete: {id}")
                        try:
                            result = await session.execute(select(User).where(User.id == id))
                            user_to_delete = result.scalars().first()
                            if not user_to_delete:
                                raise HTTPException(f"Пользователь c id({id}) не найден")
                            result = await session.execute(delete(User).where(User.id == id))
                            await session.commit()
                            logger.warning(f"delete_result: {result}")
                            result_message = f"""Удален пользователь:
                                                   <b>id:</b> {user_to_delete.id}
                                                   <b>email:</b> {user_to_delete.email}
                                                   <b>ФИО:</b> {user_to_delete.full_name}
                                                   <b>Пароль:</b> {user_to_delete.password}
                                                   <b>Статус:</b> {("Пользователь", "Админ")[user_to_delete.is_admin]}"""
                        except Exception as e:
                            result_message = f"""Ошибка удаления пользователя: 
                                                {e.args}"""
                            logger.warning(f"Ошибка удаления пользователя: {e.args}")
                    template = env.get_template('user-delete.html')
                    html_content = template.render(user_id=cur_user_id, result_message=result_message)
                    return html(html_content)
                else:
                    html_content = env.get_template('forbidden.html').render()
                    return html(html_content)
        else:
            html_content = env.get_template('forbidden.html').render()
            return html(html_content)
