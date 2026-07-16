import bcrypt
from sqlalchemy.orm import Session

from models import User


# تشفير كلمة المرور
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


# التحقق من كلمة المرور
def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )


# إنشاء مستخدم جديد
def create_user(
    db: Session,
    username,
    email,
    password,
    age,
    weight,
    height,
    level,
    goal
):

    existing = db.query(User).filter(
        (User.username == username) |
        (User.email == email)
    ).first()

    if existing:
        return None

    user = User(
        username=username,
        email=email,
        password=hash_password(password),
        age=age,
        weight=weight,
        height=height,
        fitness_level=level,
        goal=goal
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


# تسجيل الدخول
def login_user(db: Session, username, password):

    user = db.query(User).filter(
        User.username == username
    ).first()

    if not user:
        return None

    if verify_password(password, user.password):
        return user

    return None
