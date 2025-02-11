from sanic import Blueprint
from sanic.response import json
from sqlalchemy import select
from app.database import async_session
from app.models import Payment, Account
from app.config import Config
import hashlib

# Blueprint для маршрутов платежей
payment_bp = Blueprint("payment_routes", url_prefix="/payment")


@payment_bp.route('/webhook', methods=['POST'])
async def webhook(request) -> json:
    """
    Функция обработки платежей от сторонней платежной системы

    :param request:
    :return: результат выполнения транзакции
    """
    data = request.json
    signature = data.pop('signature')
    sorted_data = sorted(data.items(), key=lambda x: x[0])
    concat_values = ''.join([str(v) for k, v in sorted_data]) + Config.SECRET_KEY
    expected_signature = hashlib.sha256(concat_values.encode()).hexdigest()

    if signature != expected_signature:
        return json({"error": "Invalid signature"}, status=400)

    async with async_session() as session:
        result = await session.execute(select(Account).where(Account.id == int(data['account_id'])))
        account = result.scalars().first()
        if not account:
            account = Account(id=data['account_id'], user_id=data['user_id'], balance=0.0)
            session.add(account)

        result = await session.execute(select(Payment).where(Payment.transaction_id == data['transaction_id']))
        if result.scalars().first():
            return json({"error": "Transaction already processed"}, status=400)

        payment = Payment(
            transaction_id=data['transaction_id'],
            account_id=data['account_id'],
            user_id=data['user_id'],
            amount=data['amount']
        )
        session.add(payment)
        account.balance += data['amount']
        await session.commit()

    return json({"success": "Transaction successfully processed"})
