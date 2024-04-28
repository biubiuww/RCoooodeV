# app/models.py
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum as EnumColumn
from enum import Enum
db = SQLAlchemy()

class TimeEnum(Enum):
    DAY = 'day'
    WEEK = 'week'
    MONTH = 'month'
    COUNT = 'count'

class TypeEnum(Enum):
    TIME = 'time'
    DELAY = 'delay'
    USAGE = 'usage'

# 定义注册码属性模型
class CodeProperty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    unit = db.Column(EnumColumn(TimeEnum), nullable=False)
    value = db.Column(db.Integer, nullable=False)
    type = db.Column(EnumColumn(TypeEnum), nullable=False)
    codes = db.relationship('RegistrationCode', backref='code_property', lazy=True)

    def __repr__(self):
        return f"CodeProperty(name='{self.name}', unit='{self.unit}', value='{self.value}')"

class Renewal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(EnumColumn(TypeEnum), nullable=False)
    value = db.Column(db.Integer, nullable=False)
    registration_code_id = db.Column(db.Integer, db.ForeignKey('registration_code.id'), nullable=False)


class RegistrationCode(db.Model):
    """
    注册码模型
    Attributes:
        code: 注册码
        type: 注册码类型：
            时间生效类型(time:创建时间+时间周期=过期时间，delay:首次使用+时间周期=过期时间)
            使用次数生效类型(usage：使用次数生效)
        expiration_date: 有效期截止日期（如果注册码是时间生效类型）
        max_usage: 最大使用次数（如果注册码是使用次数生效类型）
        usage_count: 已使用次数
        status: 状态表示(True 有效, False 无效)
    """
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    type = db.Column(EnumColumn(TypeEnum), nullable=False)
    # type = db.Column(db.String(10), nullable=False)  
    expiration_date = db.Column(db.DateTime, nullable=True)  
    max_usage = db.Column(db.Integer, nullable=True)  
    usage_count = db.Column(db.Integer, default=0)  
    status = db.Column(db.Boolean, default=True)
    property_id = db.Column(db.Integer, db.ForeignKey('code_property.id'), nullable=False)
    renewals = db.relationship('Renewal', backref='registration_code', lazy=True)

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