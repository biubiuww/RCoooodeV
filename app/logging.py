# app/logging.py

import os
from datetime import datetime

# 记录注册码使用日志
def log_registration_code_usage(code, params, ip_address):
    log_directory = 'logs'
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    log_file_path = os.path.join(log_directory, f"{datetime.now().strftime('%Y-%m-%d')}.log")
    with open(log_file_path, 'a') as f:
        f.write(f"Time: {datetime.now()}, Code: {code}, Params: {params}, IP: {ip_address}\n")
