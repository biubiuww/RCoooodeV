# app/__init__.py

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


from sqlalchemy import inspect
from .config import config
from .views import web_bp,login_manager

from .models import db




def create_app():
    # 创建 Flask 应用
    app = Flask(__name__)
    app.config.from_object(config['default'])

    # 注册蓝图
    app.register_blueprint(web_bp)

    login_manager.init_app(app)
    # 初始化数据库
    db.init_app(app)

    # 导入模型，避免循环引用
    from app.models import User

    # 创建所有模型对应的表
    with app.app_context():
        meta = db.metadata
        inspector = inspect(db.engine)
        existing_tables = inspector.get_table_names()
        model_tables = [table.name for table in meta.tables.values()]
        for table_name in model_tables:
            if table_name not in existing_tables:
                meta.tables[table_name].create(db.engine)
                print(f"Table '{table_name}' created.")
        print("All tables are up to date.")

        # 检查日志文件夹是否存在，如果不存在则创建
        log_directory = app.config['LOG_DIRECTORY']
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)

        # 使用配置中的管理员账号密码初始化管理员账号密码
        admin_username = app.config['ADMIN_USERNAME']
        admin_password = app.config['ADMIN_PASSWORD']
        admin_email = app.config['ADMIN_EMAIL']
        admin = User.query.filter_by(email=admin_email).first()
        if not admin:
            admin = User(email=admin_email, password=admin_password,is_admin=True)
            db.session.add(admin)
            db.session.commit()

    return app

