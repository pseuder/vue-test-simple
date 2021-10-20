#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
"""
當出現permission denied for table或無法寫入資料庫時使用
使用時可先關閉排程器以免被空DB覆蓋
"""
import os
import license_server

# 取得目前Heroku上的資料
license_server.update_localDB_from_postgresql()
license_server.update_licenseDB_from_localDB()

# 將最新資料寫到CSV
license_server.write_csv_from_db()

# 將最新CSV推到Heroku
license_server.push_heroku()

# 清空Heroku DB
os.system(f'heroku pg:reset DATABASE_URL')

# 建立新DB
os.system(f'heroku run python3 manage.py makemigrations')
os.system(f'heroku run python3 manage.py migrate')
os.system(f'heroku run python write_model_from_csv.py -w')