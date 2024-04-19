# app/views.py
from datetime import datetime

from flask import render_template, request, jsonify, redirect, url_for, flash,Blueprint
from flask_login import current_user, login_user, logout_user, login_required, LoginManager

from .uti import generate_and_store_registration_code,verify_registration_code
from .logging import log_registration_code_usage
from .models import AdminUser


login_manager = LoginManager()

web_bp = Blueprint('views', __name__,template_folder='templates')


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
    
    if request.method == 'POST':
        data = request.get_json()
        code_type = data.get('code_type')
        expiration_date_str = data.get('expiration_date')
        max_usage = data.get('max_usage')
        if code_type == 'time':
            if expiration_date_str is not None:
                expiration_date_str = expiration_date_str[:-1]
                expiration_date = datetime.strptime(expiration_date_str, '%Y-%m-%dT%H:%M:%S.%f')
            else:
                expiration_date = None
        elif code_type == 'usage':
            expiration_date = None
        code = generate_and_store_registration_code(code_type, expiration_date, max_usage)
        return {'message': 'Create registration code.','code':code}, 200
    return render_template('admin/generate_code.html')

# 注册码验证页面路由
@web_bp.route('/verify', methods=['POST','GET'])
def verify_code():
    if request.method == 'GET':
        return render_template('verify_code.html')
    elif request.method == 'POST':
        data = request.get_json()
        code = data.get('code')
        response, status_code = verify_registration_code(code)
        return jsonify(response), status_code

 

# 从数据库中加载用户
@login_manager.user_loader
def load_user(user_id):
    return AdminUser.query.get(user_id)

# 管理员登录页面路由
@web_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(request.args.get('next') or url_for('views.admin_dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = AdminUser.query.filter_by(username=username).first()
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
