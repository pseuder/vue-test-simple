#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
# ------------------ 信件 --------------------
# 寄件者帳號(不含@之後地址)
Sender_email_account = 'eastek.intern2021@gmail.com'
# 寄件者密碼
Sender_email_password = 'Eastek.2021'
# 主旨 - 申請確認信 (to 申請人)
handle_applicant_title = '[License test] Confirmation '
# 主旨 - 申請審核通知信 (to 審核人)
handle_verify_title = '[License test] Verification '
# 主旨 - 審核結果信
result_title = '[License test] Result '
# 主旨 - 錯誤通知信
error_report_title = '[License test] Error_Report '
# 主旨 - 新帳號申請通知信
new_account_application_title = '[License test] 帳號申請! '
# 主旨 - 新帳號審核後通知信
new_account_verification_title = '[License test] 帳號申請成功! '
# 主旨 - 下載通知
download_alert_title = '[License test] 下載資料通知 '
# 主旨 - 即將過期
expiring_title = '[License Request] Expiring Soon  '
# 主旨 - 已經過期
expired_title = '[License Request] License expired  '
# 主旨 - 自動延期
auto_extension_title = '[License Request] Auto Extension'

# ---------------- 審核機制 ------------------
verify_group = ['審核-產品','審核-財務']#審核群組
verify_num = 1#審核人數
verify_user = ['admin']
verify_check = {'verify_group':[False,False], 'verify_num':0}
administrator = 'frankyeh(frank@eastek.com.tw)'

# ---------------- heroku  ------------------
app_name = "license-web-test"
# heroku 帳號若更改，可參考 license_server_use.docx 取得新參數
host = 'ec2-23-21-4-176.compute-1.amazonaws.com'
user = 'nouqjxblaofnqz'
dbname = 'ddrcmom32nva8c'
password = '7059414092e8123a0d847e54dab04a14854df92c735796e73647052cac9dc108'

# ---------------- 資料更新 ----------------
# license DB name(path: /public/static)
license_DB = "new_202105041154"
bitbucket_user = ""
bitbucket_pwd = ""
bitbucket_team = ""
bitbucket_db_repo = ""
bitbucket_license_repo = ""

# ---------------- 提醒頻率(請用;區隔) ----------------
expiring_soon_date = "28;15;7;6;5;4;3;2;1;0"
expired_date = "1;5;10;28"

