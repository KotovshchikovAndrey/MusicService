from datetime import UTC

from adapters.driven.sql.models.user import User as UserModel
from domain.models.entities.user import User
from domain.models.values.email import Email


def map_to_user(user_model: UserModel) -> User:
    return User(
        id=user_model.id,
        email=Email(user_model.email),
        is_active=user_model.is_active,
        created_at=user_model.created_at.replace(tzinfo=UTC),
    )


def map_to_insert_user_values(user: User) -> dict:
    return {
        "id": user.id,
        "email": user.email.value,
        "is_active": user.is_active,
        "created_at": user.created_at.replace(tzinfo=None),
    }
