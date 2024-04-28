# app/views.py
from datetime import datetime

from flask import render_template, request, jsonify, redirect, url_for, flash,Blueprint
from flask_login import current_user, login_user, logout_user, login_required, LoginManager

from .uti import *
from .logging import log_registration_code_usage
from .models import User,RegistrationCode, CodeProperty

login_manager = LoginManager()

web_bp = Blueprint('views', __name__, template_folder='templates')


# 网站首页路由
@web_bp.route('/')
def index():
    return render_template('index.html')

# 注册码生成页面路由
@web_bp.route('/generate_code', methods=['GET', 'POST'])
def generate_code():
    # if not current_user.is_authenticated or current_user.get_id() != 'admin':
    if not current_user.is_authenticated:
        return redirect(url_for('views.login'))
    
    if not current_user.is_admin:
        return "You are not authorized to access this page.", 403  # 返回403错误表示权限不足
        
    if request.method == 'POST':
        data = request.get_json()
        property_id = data.get('property_id')
        property = CodeProperty.query.get(property_id)
        if property is None:
            return "Invalid property ID", 400
        if property.type == 'time':
            if property.unit == 'day':
                expiration_date = datetime.now() + timedelta(days=property.value)
            elif property.unit == 'week':
                expiration_date = datetime.now() + timedelta(weeks=property.value)
            elif property.unit == 'month':
                expiration_date = datetime.now() + timedelta(days=(property.value * 30))
            property.value = None
        elif property.type == 'delay':
            code = generate_and_store_registration_code(property.type,property_id)
        code = generate_and_store_registration_code(property.type, expiration_date, property.value)
        return {'message': 'Create registration code.','code':code}, 200
    properties = CodeProperty.query.all()
    properties = [(str(property.id), 
                              property.name.split('.')[-1], 
                              str(property.unit), 
                              property.value, 
                              str(property.type).split('.')[-1]) for property in properties]
    return render_template('admin/admin_code_generate.html',properties=properties)

# 注册码验证页面路由
@web_bp.route('/verify', methods=['POST','GET'])
def verify_code():
    if request.method == 'GET':
        return render_template('code_verify.html')
    elif request.method == 'POST':
        data = request.get_json()
        code = data.get('code')
        response, status_code = verify_registration_code(code)
        return jsonify(response), status_code

#  注册码列表页面路由
@web_bp.route('/code_list', methods=['GET', 'POST'])
def code_list():
    if not current_user.is_authenticated:
        return redirect(url_for('views.login'))
    
    if not current_user.is_admin:
        return "You are not authorized to access this page.", 403  # 返回403错误表示权限不足
        
    if request.method == 'POST':
        code_id = request.form['code_id']
    page = request.args.get('page', 1, type=int)
    per_page = 10
    codes = RegistrationCode.query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template('admin/admin_code_list.html', codes=codes)

# 注册码属性创建页面路由
@web_bp.route('/edit_property', methods=['GET', 'POST'])
def edit_property():
    if request.method == 'POST':
        data = request.get_json()
        if data.get('property_id') is not None:
            property_id = data.get('property_id')
            name = data.get('name').strip()
            unit = data.get('unit').strip().upper()
            value = data.get('value').strip()
            type = data.get('type').strip().upper()
            response, status_code = update_property(property_id, name=name, unit=unit, value=value, type=type)
            return jsonify(response), status_code
        else:
            name = data.get('name').strip()
            unit = data.get('unit').strip().upper()
            value = data.get('value').strip()
            type = data.get('type').strip().upper()
            response, status_code = save_property(name, unit, value, type)
            return jsonify(response), status_code
        
    page = request.args.get('page', 1, type=int)
    per_page = 10
    pagination = CodeProperty.query.paginate(page=page, per_page=per_page, error_out=False)
    properties = pagination.items
    properties = [(str(property.id), property.name, str(property.unit), property.value, str(property.type)) for property in properties]
    
    return render_template('admin/admin_code_property.html', properties=properties, pagination=pagination)

# 从数据库中加载用户
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# 管理员登录页面路由
@web_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(request.args.get('next') or url_for('views.admin_dashboard'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.verify_password(password):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(request.args.get('next') or url_for('views.admin_dashboard'))
        flash('Invalid username or password.', 'error')
    return render_template('admin/login.html')

# 管理员登出路由
@web_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('views.login'))

# 管理员管理页面路由
@web_bp.route('/admin')
@login_required
def admin_dashboard():
    return render_template('admin/admin_dashboard.html')
