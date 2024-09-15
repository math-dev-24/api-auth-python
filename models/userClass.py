from sqlalchemy.orm import Mapped, mapped_column
from models.bdd import db


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]
    password: Mapped[str]

    @staticmethod
    def get_users():
        users = User.query.all()
        return [user.to_dict() for user in users]

    @staticmethod
    def get_user_by_email(email: str):
        return User.query.filter_by(email=email).first()

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password': self.password
        }
