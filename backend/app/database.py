from typing import TYPE_CHECKING
from flask_sqlalchemy import SQLAlchemy

if TYPE_CHECKING:
    from sqlalchemy.orm import Session
    from sqlalchemy.orm import ScopedSession

    class CustomSQLAlchemy(SQLAlchemy):
        session: Session | ScopedSession

    db = CustomSQLAlchemy()
else:
    db = SQLAlchemy()