from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class HashPassword:
    @staticmethod
    def hash(password: str) -> str:
        return password_context.hash(password)

    @staticmethod
    def verify(password: str, hashed_password: str) -> bool:
        return password_context.verify(password, hashed_password)
