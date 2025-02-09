from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import Config

# Создаем асинхронный движок для подключения к PostgreSQL
engine = create_async_engine(
    Config.DATABASE_URL,  # URL базы данных из конфигурации
    echo=True,  # Логирование SQL-запросов (можно отключить в production)
    future=True,  # Используем новые возможности SQLAlchemy 2.0
)

# Создаем фабрику сессий
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Отключаем автоматическое завершение транзакций
)

# Базовый класс для моделей
Base = declarative_base()


# Функция для получения сессии
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
