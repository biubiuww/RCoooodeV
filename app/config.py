# app/config.py
import os
base_path = os.path.dirname(os.path.abspath(__file__))

class Config:
    SECRET_KEY = 'XXYY'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    LOG_DIRECTORY = 'logs'

    ADMIN_USERNAME = 'admin'
    ADMIN_EMAIL = 'admin@admin.com'
    ADMIN_PASSWORD = 'password'


class DevelopmentConfig(Config):
    # 开发环境配置
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI') or \
                              'sqlite:///../database.db'

class ProductionConfig(Config):
    # 生产环境配置
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DATABASE_URI') or \
                              'sqlite:///../database.db'
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}