#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
import pytz
from datetime import datetime
import sqlite3
import traceback
import sys

#module
import variable
import send_email

# 報錯訊息通知decorator
def error_report(func):
    def warp(*args):
        try:
            return func(*args)
        except Exception as e:
            print("Error occur!")
            tb = sys.exc_info()[-1]
            stk = traceback.extract_tb(tb)[1]
            send_error_to_license_server(stk.filename, stk.lineno, stk.name, stk.line, e)
    return warp


# 寄給license server監控信箱
def send_error_to_license_server(error_file, error_line_no, error_func_name, error_line, e):
    utc_tz = pytz.timezone('Asia/Taipei')
    local_datetime = datetime.now(tz=utc_tz)
    local_datetime = str(local_datetime).split('.')[0]
    log_msg = f'時間: {local_datetime}<br>錯誤位置: File "{error_file}",    line {error_line_no},\
        in {error_func_name}<br>  {error_line}<br>錯誤訊息: {e}<br><br>'
    
    result = send_email.SendMessage(variable.Sender_email_account, '', 'error_report', log_msg)
    if result == 'error':
        print("郵件傳送失敗!")
    else:
        print("郵件傳送成功!")



#發送Error_Report給RD群組
def send_RD_email(error_report_content):
    RD_group = []
    local_database = sqlite3.connect("db.sqlite3")
    local_cursor = local_database.cursor()
    local_cursor.execute("SELECT members FROM groups WHERE name='Error notification'")
    members = local_cursor.fetchone()[0]
    members = eval(members)
    for mem in members:
        local_cursor.execute(f"SELECT email FROM users WHERE id='{mem}'")
        RD_group.append(local_cursor.fetchone()[0])
    
    utc_tz = pytz.timezone('Asia/Taipei')
    local_datetime = datetime.now(tz=utc_tz)
    local_datetime = str(local_datetime).split('.')[0]

    Subject = variable.error_report_title + local_datetime
    cc = ';'.join(RD_group)

    result = send_email.SendMessage(variable.Sender_email_account, cc, Subject, error_report_content)
    if result == 'error':
        print("郵件傳送失敗!")
    else:
        print("郵件傳送成功!")
