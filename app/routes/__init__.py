from .user_routes import user_bp
from .crud_routes import crud_bp
from .payment_routes import payment_bp

__all__ = ["user_bp", "crud_bp", "payment_bp"]
