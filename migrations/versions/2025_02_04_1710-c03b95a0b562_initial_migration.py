"""Initial migration

Revision ID: c03b95a0b562
Revises: 
Create Date: 2025-02-04 17:10:29.574178+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer, Float
from app.encrypting import hash_password

# revision identifiers, used by Alembic.
revision: str = 'c03b95a0b562'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def create_test_data(op) -> None:
    # Создаем объекты для вставки данных
    users_table = table(
        'users',
        column('id', Integer),
        column('email', String),
        column('password', String),
        column('full_name', String),
        column('is_admin', Integer),
    )
    accounts_table = table(
        'accounts',
        column('id', Integer),
        column('user_id', Integer),
        column('balance', Float),
    )

    # Вставляем тестового пользователя
    op.bulk_insert(users_table, [
        {
            # "id": 1,
            "email": "user@example.com",
            "password": hash_password("user123"),
            "full_name": "Test User",
            "is_admin": 0,
        }
    ])

    # Вставляем счет тестового пользователя
    op.bulk_insert(accounts_table, [
        {
            # "id": 1,
            "user_id": 1,
            "balance": 100.0,
        }
    ])

    # Вставляем тестового администратора
    op.bulk_insert(users_table, [
        {
            # "id": 2,
            "email": "admin@example.com",
            "password": hash_password("admin123"),
            "full_name": "Test Admin",
            "is_admin": 1,
        }
    ])


def upgrade() -> None:
    # Создаем таблицы
    op.create_table('users',
                    sa.Column('id', sa.Integer(), primary_key=True, nullable=False, autoincrement=True),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('full_name', sa.String(), nullable=False),
                    sa.Column('is_admin', sa.Integer(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    op.create_table('accounts',
                    sa.Column('id', sa.Integer(), primary_key=True, nullable=False, autoincrement=True),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('balance', sa.Float(), nullable=True),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('payments',
                    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
                    sa.Column('transaction_id', sa.String(), nullable=False),
                    sa.Column('account_id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('amount', sa.Float(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.ForeignKeyConstraint(['account_id'], ['accounts.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('transaction_id')
                    )

    create_test_data(op)


def downgrade() -> None:
    # Удаляем таблицы
    op.drop_table('payments')
    op.drop_table('accounts')
    op.drop_table('users')
