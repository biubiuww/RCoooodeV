# app/models.py
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from enum import Enum
db = SQLAlchemy()

class RegistrationCodeType(Enum):
    TIME_INSTANT = 1
    TIME_DELAYED = 2
    QUANTITY = 3


# 定义注册码模型
class RegistrationCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    # type = db.Column(db.Enum(RegistrationCodeType), nullable=False)
    type = db.Column(db.String(10), nullable=False)  # 时间生效类型或使用次数生效类型
    expiration_date = db.Column(db.DateTime)  # 有效期截止日期
    max_usage = db.Column(db.Integer)  # 最大使用次数
    usage_count = db.Column(db.Integer, default=0)  # 已使用次数
    status = db.Column(db.Integer, default=1)   # 状态：0 无效 1 有效

    def __repr__(self):
        return f"RegistrationCode(code='{self.code}', type='{self.type}', status='{self.status}')"

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    # username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    _password_hash = db.Column(db.String(128), nullable=False)  # 存储密码哈希值

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute.')

    @password.setter
    def password(self, password):
        # 使用 Werkzeug 生成密码哈希值并存储
        self._password_hash = generate_password_hash(password)

    def verify_password(self, password):
        # 检查密码哈希值是否匹配
        return check_password_hash(self._password_hash, password)