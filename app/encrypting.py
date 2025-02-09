import bcrypt
import logging

logger = logging.Logger(__name__)


def hash_password(password: str) -> str:
    """
    Функция для хэшированния пароля

    :param password: Пароль
    :return: хэшированный пароль
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()


def check_password(password: str, hashed_password: str) -> bool:
    """
    Функция для сравнения принятого пароля с хэшированным паролем

    :param password: принятый Пароль
    :param hashed_password: хэшированный Пароль
    :return: True/False - Пароли идентичны/нет
    """
    return bcrypt.checkpw(password.encode(), hashed_password.encode())
