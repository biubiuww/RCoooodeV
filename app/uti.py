# uti.py

import random
import string
from datetime import datetime
from .models import RegistrationCode,db



# 生成随机注册码
def generate_registration_code(length=10):
    characters = string.ascii_letters + string.digits
    code = ''.join(random.choice(characters) for _ in range(length))
    return code

# 生成注册码并存储到数据库
def generate_and_store_registration_code(code_type, expiration_date=None, max_usage=None):
    code = generate_registration_code()
    new_code = RegistrationCode(
        code=code,
        type=code_type,
        expiration_date=expiration_date,
        max_usage=max_usage
    )
    db.session.add(new_code)
    db.session.commit()
    return new_code.code


def verify_registration_code(code):
    """
    验证注册码的有效性并返回相应的状态信息。

    Args:
        code (str): 待验证的注册码。

    Returns:
        dict: 包含状态信息的字典。
    
    Valid:
        True:  有效
        False: 无效
    """
    registration_code = RegistrationCode.query.filter_by(code=code).first()
    
    # 3.9以上取消datetime.utcnow()
    # import pytz
    # utc_time = datetime.now(tzinfo=pytz.utc)

    if not registration_code:
        return {'valid': False, 'message': '无效的注册码'}, 404

    elif registration_code.type == 'time':
        if registration_code.expiration_date and registration_code.expiration_date < datetime.utcnow():

            return {'valid': False, 'message': '注册码已过期'}, 403
        else:
            return {'valid': True, 'message': '验证通过', 'expiration_date': registration_code.expiration_date}, 200

    elif registration_code.type == 'usage':
        if registration_code.max_usage and registration_code.max_usage <= 0:
            return {'valid': False, 'message': '注册码已达到最大使用次数。'}, 403
        else:
            return {'valid': True, 'message': '验证通过', 'max_usage': registration_code.max_usage, 'usage_count': registration_code.usage_count}, 200


# 更新注册码属性
def update_registration_code(registration_code_id, **kwargs):
    registration_code = RegistrationCode.query.get(registration_code_id)
    if registration_code:
        for key, value in kwargs.items():
            if hasattr(registration_code, key):
                setattr(registration_code, key, value)
        db.session.commit()
        return True
    return False
    #     return {"message": "Registration code updated successfully", "status_code": 200}
    # return {"message": "Registration code not found", "status_code": 404}