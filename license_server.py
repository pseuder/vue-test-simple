#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase #用於承載附檔
from email.mime.text import MIMEText
from email import encoders #用於附檔編碼
import time
from datetime import datetime, timedelta, timezone, date
import os, json, csv, codecs
import psycopg2, sqlite3
import httplib2, base64
from googleapiclient import discovery

# module
import variable
import repo_update
import error_report_module
import send_email
import get_email

def get_postgresql_coonection():
    ###連接heroku_database###
    sslmode = 'require'
    conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(
                    variable.host, variable.user, variable.dbname, variable.password, sslmode)
    conn = psycopg2.connect(conn_string)
    print("Connection postgresql success")
    return conn

###本地端同步heroku database###
def update_localDB_from_postgresql():
    conn = get_postgresql_coonection()
    web_cursor = conn.cursor()
    web_cursor.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'""")
    tables = web_cursor.fetchall()
    web_table = []
    for table in tables:
        web_table.append(table[0])

    ###連接local_database###
    local_database = sqlite3.connect("db.sqlite3")
    local_cursor = local_database.cursor()
    local_cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    local_Tables = local_cursor.fetchall()

    #將本地DB改為Heroku Postgres
    for table in local_Tables:
        if table[0] in web_table:
            #將local_DB資料刪除
            local_cursor.execute('DELETE FROM '+ table[0]+';',)
            #獲取local_DB table內各行名稱
            local_cursor.execute("SELECT * FROM {}".format(table[0]))
            #為了符合sql語法 Ex:sqlite_sequence(name,seq)
            table_detail = str(tuple([tuple[0] for tuple in local_cursor.description]))
            #為了符合sql語法 Ex:sqlite_sequence(:name,:seq)
            table_type = str(tuple([(':'+tuple[0]) for tuple in local_cursor.description])).replace("'",'')
            #獲取web_local資料
            web_cursor.execute("SELECT * FROM "+table[0])
            myresult = web_cursor.fetchall()
            for web_table_data in myresult:
                local_cursor.execute("INSERT INTO "+table[0]+table_detail+"VALUES"+table_type, web_table_data)
    local_database.commit()
    print("local database update done")


###license database同步local database###
def update_licenseDB_from_localDB():
    license_tables = ['customers', 'info', 'modules', 'options', 'product_groups', 'products', 'region', 'sn']
    # local database connection
    local_conn = sqlite3.connect("db.sqlite3")
    local_cur = local_conn.cursor()

    # license database connection
    license_conn = sqlite3.connect(f"public/static/{variable.license_DB}")
    license_cur = license_conn.cursor()

    #將license DB改為local DB
    for table in license_tables:
            #將license_DB資料刪除
            license_cur.execute('DELETE FROM '+ table+';',)
            #獲取license_DB table內各行名稱
            license_cur.execute("SELECT * FROM {}".format(table))
            #為了符合sql語法 Ex:sqlite_sequence(name,seq)
            table_detail = str(tuple([tuple[0] for tuple in license_cur.description]))
            #為了符合sql語法 Ex:sqlite_sequence(:name,:seq)
            table_type = str(tuple([(':'+tuple[0]) for tuple in license_cur.description])).replace("'",'')
            #獲取web_local資料
            local_cur.execute("SELECT * FROM "+table)
            myresult = local_cur.fetchall()
            for web_table_data in myresult:
                # license DB 和local DB 欄位不太一樣
                if table == 'info':
                    web_table_data = list(web_table_data)
                    version = web_table_data.pop(3)
                    web_table_data.append(version)
                license_cur.execute("INSERT INTO "+table+table_detail+"VALUES"+table_type, web_table_data)
    license_conn.commit()
    print("license database update done")

def update_localDB_and_herokuDB_from_verifyData(verify_data):
    # heroku database connection
    web_conn = get_postgresql_coonection()
    web_cur = web_conn.cursor() 

    # local database connection
    local_conn = sqlite3.connect("db.sqlite3")
    local_cur = local_conn.cursor()

    complete_app_data = []

    #避免新增到重覆的*AGENT_EST_ID
    agent_dict = {}
    for app_data in verify_data['data']:
        agent_dict[str(app_data['sn'])] = []
        # 增加多筆展延、刪除資料
        if app_data['operator'] == '多筆展延':
            if app_data['verify'] == "√":
                local_cur.execute(f"SELECT * FROM info WHERE sn='{app_data['sn']}'")
                info_all = local_cur.fetchall()
                for info in info_all:
                    multi_oper_data = {}
                    product_name = ''
                    multi_oper_data['info_id'] = info[0]
                    multi_oper_data['sn'] = info[1]
                    multi_oper_data['func_uid'] = info[2]
                    module = ''
                    category = ''
                    product = ''
                    local_cur.execute(f"SELECT product_name, caption FROM options WHERE option_name ='{info[2]}'")
                    fetch_options = local_cur.fetchone()
                    # func_uid在option內
                    if fetch_options:
                        product_name = fetch_options[0]
                        module = fetch_options[1]
                        local_cur.execute(f"SELECT category_id, caption FROM products WHERE product_name ='{product_name}'")
                        fetch_products = local_cur.fetchone()
                        if fetch_products:
                            category = fetch_products[0]
                            product = fetch_products[1]
                        else:
                            category = ''
                            product = ''

                    # func_uid在product內
                    if product_name == '':
                        local_cur.execute(f"SELECT category_id, caption FROM products WHERE product_name ='{info[2]}'")
                        fetch_products = local_cur.fetchone()
                        if fetch_products:
                            module = ''
                            category = fetch_products[0]
                            product = fetch_products[1]

                    # func_uid皆無對應
                    if product == '':
                        module = ''
                        category = ''
                        product = info[2]

                    multi_oper_data['category'] = category
                    multi_oper_data['product'] = product
                    multi_oper_data['module'] = module
                    multi_oper_data['version'] = info[3]
                    multi_oper_data['issued'] = info[4]
                    multi_oper_data['expiration'] = app_data['expiration']
                    multi_oper_data['count'] = info[6]
                    multi_oper_data['registration'] = info[7]
                    local_cur.execute(f"SELECT caption FROM modules WHERE mod_uid='{info[8]}'")
                    multi_oper_data['type'] = local_cur.fetchone()[0]
                    multi_oper_data['comment'] = info[9]
                    multi_oper_data['contact'] = info[10]
                    multi_oper_data['user'] = app_data['user']
                    multi_oper_data['region'] = app_data['region']
                    multi_oper_data['operator'] = '修改'
                    multi_oper_data['verify'] = app_data['verify']
                    multi_oper_data['reason'] = app_data['reason']
                    complete_app_data.append(multi_oper_data)
        elif app_data['operator'] == '多筆刪除':
            if app_data['verify'] == "√":
                local_cur.execute(f"SELECT * FROM info WHERE sn='{app_data['sn']}'")
                info_all = local_cur.fetchall()
                for info in info_all:
                    multi_oper_data = {}
                    multi_oper_data['info_id'] = info[0]
                    multi_oper_data['sn'] = info[1]
                    multi_oper_data['func_uid'] = info[2]
                    multi_oper_data['version'] = info[3]
                    multi_oper_data['issued'] = info[4]
                    multi_oper_data['expiration'] = info[5]
                    multi_oper_data['count'] = info[6]
                    multi_oper_data['registration'] = info[7]
                    local_cur.execute(f"SELECT caption FROM modules WHERE mod_uid='{info[8]}'")
                    multi_oper_data['type'] = local_cur.fetchone()[0]
                    multi_oper_data['comment'] = info[9]
                    multi_oper_data['contact'] = info[10]
                    multi_oper_data['user'] = app_data['user']
                    multi_oper_data['region'] = app_data['region']
                    multi_oper_data['operator'] = '刪除'
                    multi_oper_data['verify'] = app_data['verify']
                    multi_oper_data['reason'] = app_data['reason']
                    complete_app_data.append(multi_oper_data)
        else:
            if app_data['verify'] == "√":
                complete_app_data.append(app_data)
    
    
    for app_data in complete_app_data:
        if app_data['verify'] == '√':
            if app_data['operator'] == "新增":
                if "AGENT_EST_ID" not in app_data['func_uid']:
                    if ("CATK_FIX" in app_data['func_uid']):
                        local_cur.execute(f"SELECT * FROM info WHERE sn='{app_data['sn']}'and func_uid='CATK_FIX_AGENT_EST_ID'")
                        if not local_cur.fetchone() and "CATK_FIX_AGENT_EST_ID" not in agent_dict[str(app_data['sn'])]:
                            new_app_data = app_data.copy()
                            new_app_data['func_uid'] = "CATK_FIX_AGENT_EST_ID"
                            new_app_data['comment'] = "系統自動增加"
                            complete_app_data.append(new_app_data)
                            agent_dict[str(app_data['sn'])].append("CATK_FIX_AGENT_EST_ID")
                    elif ("CATK_GRID" in app_data['func_uid']):
                        local_cur.execute(f"SELECT * FROM info WHERE sn='{app_data['sn']}'and func_uid='CATK_GRID_AGENT_EST_ID'")
                        if not local_cur.fetchone() and "CATK_GRID_AGENT_EST_ID" not in agent_dict[str(app_data['sn'])]:
                            new_app_data = app_data.copy()
                            new_app_data['func_uid'] = "CATK_GRID_AGENT_EST_ID"
                            new_app_data['comment'] = "系統自動增加"
                            complete_app_data.append(new_app_data)
                            agent_dict[str(app_data['sn'])].append("CATK_GRID_AGENT_EST_ID")
                    elif ("CATK_MAP" in app_data['func_uid']):
                        local_cur.execute(f"SELECT * FROM info WHERE sn='{app_data['sn']}'and func_uid='CATK_MAP_AGENT_EST_ID'")
                        if not local_cur.fetchone() and "CATK_MAP_AGENT_EST_ID" not in agent_dict[str(app_data['sn'])]:
                            new_app_data = app_data.copy()
                            new_app_data['func_uid'] = "CATK_MAP_AGENT_EST_ID"
                            new_app_data['comment'] = "系統自動增加"
                            complete_app_data.append(new_app_data)
                            agent_dict[str(app_data['sn'])].append("CATK_MAP_AGENT_EST_ID")
                    elif ("CATK_PROBE" in app_data['func_uid']):
                        local_cur.execute(f"SELECT * FROM info WHERE sn='{app_data['sn']}'and func_uid='CATK_PROBE_AGENT_EST_ID'")
                        if not local_cur.fetchone() and "CATK_PROBE_AGENT_EST_ID" not in agent_dict[str(app_data['sn'])]:
                            new_app_data = app_data.copy()
                            new_app_data['func_uid'] = "CATK_PROBE_AGENT_EST_ID"
                            new_app_data['comment'] = "系統自動增加"
                            complete_app_data.append(new_app_data)
                            agent_dict[str(app_data['sn'])].append("CATK_PROBE_AGENT_EST_ID")
                    elif ("CATK_CAR" in app_data['func_uid']):
                        local_cur.execute(f"SELECT * FROM info WHERE sn='{app_data['sn']}'and func_uid='CATK_CAR_AGENT_EST_ID'")
                        if not local_cur.fetchone() and "CATK_CAR_AGENT_EST_ID" not in agent_dict[str(app_data['sn'])]:
                            new_app_data = app_data.copy()
                            new_app_data['func_uid'] = "CATK_CAR_AGENT_EST_ID"
                            new_app_data['comment'] = "系統自動增加"
                            complete_app_data.append(new_app_data)
                            agent_dict[str(app_data['sn'])].append("CATK_CAR_AGENT_EST_ID")

                new_info_id = operator_DB(app_data, '', local_cur, web_cur)
                update_add_info(app_data, verify_data, new_info_id, local_cur, web_cur)
            elif app_data['operator'] == "修改":
                operator_DB(app_data, verify_data, local_cur, web_cur)
            elif app_data['operator'] == "刪除":
                operator_DB(app_data, '', local_cur, web_cur)
    print("operator DB done")

    contacts = set()
    test = 0
    for data in complete_app_data:
        for contact in data['contact'].split(';'):
            contacts.add(data['contact'])
        
        if data['verify'] != '√':
            local_cur.execute(f"UPDATE Application SET status = 'nopass' WHERE  id = '{verify_data['id']}'")
            web_cur.execute(f"UPDATE Application SET status = 'nopass' WHERE  id = '{verify_data['id']}'")
            test = 1
    if test == 0:
        local_cur.execute(f"UPDATE Application SET status = 'pass' WHERE  id = '{verify_data['id']}'")
        web_cur.execute(f"UPDATE Application SET status = 'pass' WHERE  id = '{verify_data['id']}'")
    #將全部改動commit
    local_conn.commit()
    web_conn.commit()
    update_licenseDB_from_localDB()
    return list(contacts)



def operator_DB(data, verify, local_cur, web_cur):
    new_info_id = 0
    local_cur.execute(f"SELECT mod_uid FROM Modules WHERE caption = '{ data['type'] }'")
    type = local_cur.fetchone()[0]

    #------psycopg2使用提示------#
    # 在psycopg2內，若使用到保留字必須使用其他寫法
    # 例：在Sn內撈取user：	
    #         cursor.execute("SELECT Sn.user FROM Sn")
    #     在Sn內更新user：	
    #         cursor.execute("UPDATE Sn SET \"user\" = 'username' WHERE sn = '123' ")
    
    ##操作DB###
    if data['operator'] == '刪除':
        local_cur.execute(f"DELETE FROM Info WHERE id = '{ data['info_id'] }'")
        web_cur.execute(f"DELETE FROM Info WHERE id = '{ data['info_id'] }'")
    elif data['operator'] == '修改':
        local_cur.execute(f"SELECT user, email FROM users")
        user_email = local_cur.fetchall()

        if '@' not in data['contact']:
            for user in user_email:
                if data['contact'] == user[0]:
                    data['contact'] = user[1]

        local_cur.execute(f"SELECT id FROM Region WHERE name = '{data['region']}'")
        fetch_Region = local_cur.fetchone()
        region = data['region']
        if fetch_Region:
            region = fetch_Region[0]
        

        local_cur.execute(f"UPDATE Sn SET region = '{region}', user = '{data['user']}' WHERE  sn = '{data['sn']}'")
        web_cur.execute(f"UPDATE Sn SET region = '{region}', \"user\" = '{data['user']}' WHERE  sn = '{data['sn']}'")
       

        #獲取info原資料和新資料紀錄
        info_info = get_modify_info(data, verify, local_cur)
        
        info_info = json.dumps(info_info, ensure_ascii=False)
        local_cur.execute(f"SELECT type FROM Info WHERE id = '{data['info_id']}'")
        origin_type = local_cur.fetchone()[0]
        #有改type的情況
        if type != origin_type:
            same_info_id = None
            local_cur.execute(f"SELECT type, func_uid, sn, id FROM Info")
            info_all = local_cur.fetchall()
            for info in info_all:
                if type == info[0] and data['func_uid'] == info[1] and data['sn'] == info[2]:
                    same_info_id = info[3]
            if same_info_id != None:#情況一type A -> B (B已存在)                             #* 做法: 
                local_cur.execute(f"DELETE FROM Info WHERE id = '{ data['info_id'] }'")      #    1. 將 A 資料刪除
                web_cur.execute(f"DELETE FROM Info WHERE id = '{ data['info_id'] }'")
                local_cur.execute(f"SELECT count FROM Info WHERE id = '{ same_info_id }'")   #    2. 將 B 資料修改(個數為 A+B 總和)
                new_info_count = int(data['count']) + local_cur.fetchone()[0]
                new_info_info = '' ###要更新的info###
                local_cur.execute(f"UPDATE Info SET count = '{new_info_count}', expiration = '{data['expiration']}' , info = '{info_info}' \
                                    , issued = '{str(date.today())}' WHERE  id = '{same_info_id}'")
                web_cur.execute(f"UPDATE Info SET count = '{new_info_count}', expiration = '{data['expiration']}' , info = '{info_info}' \
                                    , issued = '{str(date.today())}' WHERE  id = '{same_info_id}'")
            else:#情況2 type A -> B (B不存在)           ###???###                                     #* 做法: 
                local_cur.execute(f"DELETE FROM Info WHERE id = '{ data['info_id'] }'")  #    1. 將 A 資料刪除
                web_cur.execute(f"DELETE FROM Info WHERE id = '{ data['info_id'] }'")    
                
                local_cur.execute(f"SELECT * FROM Info")#    2. 新增 B 資料
                info_all = local_cur.fetchall()
                for i in range(1,len(info_all)+1):
                    local_cur.execute(f"SELECT * FROM Info WHERE id = '{i}'")
                    if local_cur.fetchone() == None:
                        sql = "INSERT INTO info(id,sn,func_uid,version,issued,expiration,count,registration,type,comment,contact,info) \
                        VALUES(?,?,?,?,?,?,?,?,?,?,?,?)"   
                        local_cur.execute(
                            sql, (i, data['sn'],data['func_uid'],data['version'],str(date.today()),data['expiration'],
                            data['count'],data['registration'],type,data['comment'],data['contact'],info_info))
                        sql = "INSERT INTO info(id,sn,func_uid,version,issued,expiration,count,registration,type,comment,contact,info) \
                            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                        web_cur.execute(
                            sql, (i, data['sn'],data['func_uid'],data['version'],str(date.today()),data['expiration'],
                            data['count'],data['registration'],type,data['comment'],data['contact'],info_info))
                        break

        #沒改type的情況
        else:
            sql = "UPDATE Info SET sn = ?, func_uid = ?, version = ?, issued = ?, expiration = ?, count = ?,\
                   registration = ?, type = ?, comment = ?, contact = ?, info = ? WHERE id = ?"
            val = (data['sn'],data['func_uid'],data['version'],str(date.today()),data['expiration'],data['count'],
                   data['registration'],type,data['comment'],data['contact'],info_info,data['info_id'])
            local_cur.execute(sql, val)
            sql = "UPDATE Info SET sn = %s, func_uid = %s, version = %s, issued = %s, expiration = %s, count = %s, \
                   registration = %s, type = %s, comment = %s, contact = %s, info = %s WHERE id = %s"
            web_cur.execute(sql, val)
    elif data['operator'] == '新增':
        local_cur.execute(f"SELECT * FROM Sn WHERE sn = '{data['sn']}'")
        #sn不存在
        if local_cur.fetchone() == None:
            customer = data['customer'].split('|')
            if len(customer) == 1:
                customer.append('')
            local_cur.execute(f"SELECT * FROM Customers WHERE name = '{customer[0]}' and site = '{customer[1]}'")
            if local_cur.fetchone() == None:
                local_cur.execute(f"SELECT * FROM Customers")
                customers_all = local_cur.fetchall()
                for i in range(1,len(customers_all)+2):
                    local_cur.execute(f"SELECT * FROM Customers WHERE id = '{i}'")
                    if local_cur.fetchone() == None:
                        local_cur.execute(f"INSERT INTO customers(id,name,site) VALUES('{i}','{customer[0]}','{customer[1]}')")
                        web_cur.execute(f"INSERT INTO customers(id,name,site) VALUES('{i}','{customer[0]}','{customer[1]}')")
                        break
            
            local_cur.execute(f"SELECT id FROM Customers WHERE name = '{customer[0]}' and  site = '{customer[1]}' ")
            sn_id = local_cur.fetchone()[0]
            local_cur.execute(f"SELECT id FROM Region WHERE name = '{data['region']}'")
            region = local_cur.fetchone()[0]
            sql = f"INSERT INTO sn(id,sn,region,user,record,note1,note2,note3,note4,note5)  VALUES(?,?,?,?,?,?,?,?,?,?)"
            local_cur.execute(sql, (sn_id, data['sn'], region, data['user'], '', '','','','',''))
            sql = f"INSERT INTO sn(id,sn,region,\"user\",record,note1,note2,note3,note4,note5)  VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            web_cur.execute(sql, (sn_id, data['sn'],region, data['user'], '', '','','','',''))
        #sn已存在
        else:
            local_cur.execute(f"SELECT id, user FROM sn WHERE  sn = '{data['sn']}'")
            sn_data = local_cur.fetchone()
            customer_id = sn_data[0]
            origin_user = sn_data[1]
            local_cur.execute(f"SELECT name FROM customers WHERE  id = '{customer_id}'")
            origin_customer = local_cur.fetchone()[0]
            #新增資料的顧客和原本相同
            if origin_customer == data['customer']:
                #更改負責人:
                if origin_user != data['user']:
                    local_cur.execute(f"UPDATE Sn SET user = '{data['user']}' WHERE  sn = '{data['sn']}'")
                    web_cur.execute(f"UPDATE Sn SET \"user\" = '{data['user']}' WHERE  sn = '{data['sn']}'")
            #新增資料的顧客和原本不同
            else:
                customer = data['customer'].split('|')
                if len(customer) == 1:
                    customer.append('')
                local_cur.execute(f"SELECT * FROM Customers WHERE name = '{customer[0]}' and site = '{customer[1]}'")
                exist_customer = local_cur.fetchone()
                #新顧客
                if exist_customer == None:
                    local_cur.execute(f"SELECT * FROM Customers")
                    customers_all = local_cur.fetchall()
                    for i in range(1,len(customers_all)+2):
                        local_cur.execute(f"SELECT * FROM Customers WHERE id = '{i}'")
                        if local_cur.fetchone() == None:
                            local_cur.execute(f"INSERT INTO customers(id,name,site) VALUES('{i}','{customer[0]}','{customer[1]}')")
                            web_cur.execute(f"INSERT INTO customers(id,name,site) VALUES('{i}','{customer[0]}','{customer[1]}')")

                            local_cur.execute(f"UPDATE Sn SET id = '{i}', user = '{data['user']}' WHERE  sn = '{data['sn']}'")
                            web_cur.execute(f"UPDATE Sn SET id = '{i}', \"user\" = '{data['user']}' WHERE  sn = '{data['sn']}'")
                            break
                #舊顧客
                else:
                    #更改負責人
                    if origin_user != data['user']:
                        local_cur.execute(f"UPDATE Sn SET id = '{exist_customer[0]}', user = '{data['user']}' WHERE  sn = '{data['sn']}'")
                        web_cur.execute(f"UPDATE Sn SET id = '{exist_customer[0]}', \"user\" = '{data['user']}' WHERE  sn = '{data['sn']}'")

        local_cur.execute(f"SELECT * FROM Info")
        info_all = local_cur.fetchall()
        for i in range(1,len(info_all)+2):
            local_cur.execute(f"SELECT * FROM Info WHERE id = '{ i }'")
            if local_cur.fetchone() == None:
                new_info_id = i
                sql = "INSERT INTO info(id,sn,func_uid,version,issued,expiration,count,registration,type,comment,contact,info) \
                       VALUES(?,?,?,?,?,?,?,?,?,?,?,?)" 
                local_cur.execute(
                    sql, (i, data['sn'],data['func_uid'],data['version'],str(date.today()),data['expiration'],data['count'],
                    str(date.today()),type,data['comment'],data['contact'],str([])))
                sql = "INSERT INTO info(id,sn,func_uid,version,issued,expiration,count,registration,type,comment,contact,info) \
                       VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" 
                web_cur.execute(
                    sql, (i, data['sn'],data['func_uid'],data['version'],str(date.today()),data['expiration'],data['count'],
                    str(date.today()),type,data['comment'],data['contact'],str([])))
                break
    
    #改DB同時更新heroku上傳時間
    update_time = generate_last_update_time() 
    local_cur.execute(f"UPDATE Updatetime SET update_time = '{update_time}' WHERE  id = 'last_update_time'")
    web_cur.execute(f"UPDATE Updatetime SET update_time = '{update_time}' WHERE  id = 'last_update_time'")

    
    if data['operator'] == '新增': return new_info_id
    else: return 0


def generate_last_update_time():
    '''生成heroku上傳時間'''
    i = datetime.now()
    i = i.astimezone(timezone(timedelta(hours=8)))#台灣時區GMT+8
    return (("%d/%02d/%02d %02d:%02d:%02d") % (i.year, i.month, i.day, i.hour, i.minute, i.second))


def get_modify_info(app_data, verify, local_cur):
    """回傳info的原資料與修改紀錄"""
    #verify['date']內包含 年-月-日 時:分:秒，目前修改紀錄只需年-月-日所以取前10個字元
    app_date = verify['date'][:10]
    app_applicant = verify['applicant']
    app_validators = verify["validator"]['verify_user']
    app_validator = "、".join(app_validators)
    
    info_info = []
    local_cur.execute(f"SELECT info, type, version, count, contact, expiration FROM Info WHERE id = '{ app_data['info_id'] }'")
    info_data = local_cur.fetchone()
    if info_data[0] != '':
        info_info = eval(info_data[0])
    
    local_cur.execute(f"SELECT caption FROM Modules WHERE mod_uid = '{ info_data[1] }'")
    origin_type = local_cur.fetchone()[0]

    product = app_data['func_uid']
    local_cur.execute(f"SELECT * FROM Options WHERE option_name = '{ app_data['func_uid'] }'")
    if local_cur.fetchone():
        local_cur.execute(f"SELECT product_name FROM Options WHERE option_name = '{ app_data['func_uid'] }'")
        product_name = local_cur.fetchone()[0]
        local_cur.execute(f"SELECT caption FROM Products WHERE product_name = '{ product_name }'")
        product = local_cur.fetchone()[0]
    elif local_cur.execute(f"SELECT caption FROM Modules WHERE mod_uid = '{ app_data['func_uid'] }'"):
        product = local_cur.fetchone()
        if product:
            product = product[0]
        else:
            product = app_data['func_uid']
    


    new_compare_data = []
    origin_data = {}
    origin_data = {'申請類別':"原資料", '產品類別':app_data['category'], '產品': product, '模組/功能':app_data['module'], 
    '版本': info_data[2],'數量': info_data[3], '類型': origin_type,'聯絡人': info_data[4], '使用期限': info_data[5]}
    new_compare_data.append(origin_data)

    new_data = {}
    new_data = {
        'ID': verify['id'], '申請日期':app_date,'申請人':app_applicant, '類型類別':"修改", '審核人':app_validator,
        '申請類別':"修改", '產品類別':app_data['category'], '產品': product, '模組/功能':app_data['module'], 
        '版本': app_data['version'],'數量': app_data['count'], '類型': app_data['type'],'聯絡人': app_data['contact'], 
        '使用期限': app_data['expiration']
    }
    new_compare_data.append(new_data)
    info_info.append(new_compare_data)
    return info_info

def update_add_info(app_data, verify, new_info_id, local_cur, web_cur):
    """更新新增操作的info"""
    app_date = verify['date'][:10]
    app_applicant = verify['applicant']
    app_validators = verify["validator"]['verify_user']
    app_validator = "、".join(app_validators)

    info_info = [] 
    new_info_info = []
   

    new_data = {
        'ID': verify['id'], '申請日期':app_date,'申請人':app_applicant, '類型類別':"新增", '審核人':app_validator,
        '申請類別':"新增", '產品類別':app_data['category'], '產品': app_data['product'], '模組/功能':app_data['module'], 
        '版本': app_data['version'],'數量': app_data['count'], '類型': app_data['type'],'聯絡人': app_data['contact'], 
        '使用期限': app_data['expiration']
    }
    new_info_info.append(new_data)
    info_info.append(new_info_info)
    new_info_data = json.dumps(info_info ,ensure_ascii=False)
    local_cur.execute(f"UPDATE Info SET info = '{new_info_data}' WHERE  id = '{new_info_id}'")
    web_cur.execute(f"UPDATE Info SET info = '{new_info_data}' WHERE  id = '{new_info_id}'")
    print("DB  modify done")

        
def create_license(db_path, target_path):
    exe_path = f'{os.getcwd()}/public/static/GenerateLicense.exe'
    os.system(f'{exe_path} {db_path} {target_path}')
    print("license create done")


#獲取application資料
def get_data(service, user_id, msg_id, applicantion_num):
    applicant = ''
    verifier = []
    verify_data = {}
    content = '審核者回覆:'
    content += get_email.get_content(service, user_id, msg_id).split('審核者回覆:')[1]
    print("email get done")

    local_database = sqlite3.connect("db.sqlite3")
    local_cursor = local_database.cursor()

    local_cursor.execute(f"SELECT * FROM application WHERE id='{applicantion_num}'")
    row_data = local_cursor.fetchone()
    applicant_column = ['id', 'date', 'applicant', 'status', 'data', 'validator', 'verify_time', 'content'] 
    for i in range(len(applicant_column)):
        if(applicant_column[i] == 'data' or applicant_column[i] == 'validator' or applicant_column[i] == 'content'):
            my_row_data = row_data[i].replace('true', '""')
            my_row_data = my_row_data.replace('false', '""')
            my_row_data = my_row_data.replace('null', '""')
            verify_data[applicant_column[i]] = eval(my_row_data)
        else:
            verify_data[applicant_column[i]] = row_data[i]
    
    applicant = verify_data['applicant']
    local_cursor.execute(f"SELECT email FROM users WHERE user='{applicant}'")
    applicant = local_cursor.fetchone()[0]

    verifiers = verify_data['validator']['verify_user']
    for v in verifiers:
        local_cursor.execute(f"SELECT email FROM users WHERE user='{v}'")
        v_email = local_cursor.fetchone()[0]
        if ("eastek@eastek.com.tw" not in v_email) and ("@gmail.com" not in v_email):
            verifier.append(v_email)
    return applicant, verifier, verify_data, content


#發送審核結果通知信
def send_result_email(content, applicant, verify_data, applicantion_num, contacts):
    message = create_message(content, verify_data, applicantion_num, applicant, contacts)
    result = send_email.SendMessage('', '', '', '', message)
    if result == 'error':
        print("郵件傳送失敗!")
    else:
        print("郵件傳送成功!")


# 根據申請人的勾選獲取審核群組
def get_verification_groups(content):
    new_key_apply = content.get('new_key_apply')
    verification_group_name = content.get('verification_group_name')
    verification_groups = set()
    verification_emails = []
    local_database = sqlite3.connect("db.sqlite3")
    local_cursor = local_database.cursor()
    local_cursor.execute(f"SELECT members FROM groups WHERE name='{verification_group_name}'")
    group_member = local_cursor.fetchone()[0]
    
    # 加入申請人勾選的審核單位
    if group_member == '':
        group_member = []
    else:
        group_member = eval(group_member)
        
    for member_id in group_member:
        verification_groups.add(member_id)

    # 加入審核-財務(如果有勾new key)
    if new_key_apply == 'yes':
        local_cursor.execute(f"SELECT members FROM groups WHERE name='finance-verification'")
        group_member = local_cursor.fetchone()[0]
        if group_member == '':
            group_member = []
        else:
            group_member = eval(group_member)
            
        for member_id in group_member:
            verification_groups.add(member_id)

    verification_groups = list(verification_groups)
    for v_id in verification_groups:
        local_cursor.execute(f"SELECT email FROM users WHERE id='{v_id}'")
        v_email = local_cursor.fetchone()[0]
        if v_email not in verification_emails:
            verification_emails.append(v_email)

    return verification_emails


#郵件內容與附件
def create_message(content, verify_data, applicantion_num, applicant, contacts):
    msg = MIMEMultipart('mixed')
    msg['Subject'] = variable.result_title + ' ' + str(applicantion_num)
    msg['From'] = variable.Sender_email_account
    msg['To'] = applicant

    verification_emails = get_verification_groups(verify_data.get('content'))

    # 使用set移除重複的信箱
    cc_set = set(contacts + verification_emails)
    cc_list = list(cc_set)

    msg["Cc"] = ';'.join(cc_list)
    msg.attach(MIMEText(content, 'html'))
    cwd = os.getcwd()
    attachments = [f'{cwd}/public/static/license']
    for file in attachments:
        try:
            with open(file, 'rb') as fp:
                filemsg = MIMEBase('application', "octet-stream")
                filemsg.set_payload(fp.read())
            encoders.encode_base64(filemsg)
            filemsg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
            msg.attach(filemsg)
        except:
            print("Unable to open the attachments.")
    print("attach email done")
    return {'raw': (base64.urlsafe_b64encode(msg.as_bytes())).decode("utf-8") }


#產生license並寄信
def work(service, user_id, labels_map):
    license_change = False
    current_path = os.getcwd()
    db_path = f'{current_path}/public/static/{variable.license_DB}'
    license_path = f'{current_path}/public/static/license'

    #傳送過的序號
    with open('sent_result_list.txt', 'r') as f:
        sent_result_list = f.read()

    error_report_content = ''
    message = service.users().messages().list(userId=user_id).execute()
    for msg_id in message['messages']:
        subject = get_email.get_subject(service, user_id, msg_id['id'])

        if "error_report" in subject:
            email_labels = get_email.get_label(service, user_id, msg_id['id'], labels_map)
            if("Error_Report" not in email_labels):
                error_report_content = get_email.get_content(service, user_id, msg_id['id'])
                error_report_module.send_RD_email(error_report_content)
                # 上標籤
                get_email.add_label(service, user_id, msg_id['id'], labels_map, 'Error_Report')

        if "send_license" not in subject:
            continue

        # 判斷合法標題:send_license_數字
        applicantion_num = subject.split('_')
        if(len(applicantion_num) == 3):
            applicantion_num = applicantion_num[-1]
        else:
            continue

        if(not applicantion_num.isdigit()):
            continue

        # 判斷是否傳送過
        if 'resend' in subject:
            email_labels = get_email.get_label(service, user_id, msg_id['id'], labels_map)
            if("Resend_License" in email_labels):
                continue
        else:
            if(applicantion_num in sent_result_list):
                break
        
        # 判斷寄信者
        if get_email.get_sender(service, user_id, msg_id['id']) != variable.Sender_email_account:
            continue
        
        
        print(f'Request email detected!:{subject}')

        license_change = True
        # 同步
        update_localDB_from_postgresql()
        update_licenseDB_from_localDB()
        #獲取修改資訊
        applicant, verifier, verify_data, content = get_data(service, user_id, msg_id['id'], applicantion_num)
        #更新DB, 回傳在申請資料內的聯絡人
        contacts = update_localDB_and_herokuDB_from_verifyData(verify_data)
        #產生license
        create_license(db_path, license_path)
        #寄送信件
        send_result_email(content, applicant, verify_data, applicantion_num, contacts)
        
        with open('sent_result_list.txt', 'a') as f:
            f.write(','+applicantion_num)

        if 'resend_license' in subject:
            get_email.add_label(service, user_id, msg_id['id'], labels_map, 'Resend_License')

    if license_change:
        #推送heroku
        write_csv_from_db()
        push_heroku()
        if ((variable.bitbucket_user) and (variable.bitbucket_pwd) 
            and (variable.bitbucket_db_repo) and (variable.bitbucket_license_repo)):
            repo_update.update(current_path, db_path, license_path)
    

def write_csv_from_db():
    database = sqlite3.connect("db.sqlite3")
    cursor = database.cursor()
    tables = ['Application','Customers','Groups', 'Info','Modules','Products','Region', 'Sn', 'Users','Edit','Product_groups','options']
    if not os.path.isdir("./csv"):
        os.mkdir("./csv")

    for table in tables:
        csv_file = codecs.open(('./csv/%s.csv') % table, 'w', encoding='utf-8')
        writer = csv.writer(csv_file)

        for row in cursor.execute("SELECT * FROM %s" % table):
            writer.writerow(row)

        csv_file.close()


def push_heroku():
    os.system(f'git add .')
    os.system(f'git commit -m "auto update DB and license"')
    os.system(f'git push')
    print("Heroku push done")



def get_result_list():
    result_list = []
    conn = get_postgresql_coonection()
    web_cursor = conn.cursor()
    web_cursor.execute("SELECT id, status FROM application")
    app_info = web_cursor.fetchall()
    for app in app_info:
        if app[1] == 'pass' or app[1] == 'nopass':
            result_list.append(app[0])
    #最新的result_list
    with open('sent_result_list.txt', 'w') as f:
        f.write(str(result_list)[1:-1])


if __name__ == '__main__':
    credentials = get_email.get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    user_id='me'
    # 對照標籤id->name
    labels_map = {}
    labels = service.users().labels().list(userId=user_id).execute()
    for lab in labels['labels']:
        labels_map[lab['id']] = lab['name']
    
    #license server 啟動
    pid = str(os.getpid())
    with open('license_server.pid', 'w') as f:
        f.write(pid)
    try:
        #首次執行先同步heroku DB
        update_localDB_from_postgresql()
        update_licenseDB_from_localDB()
        #取得sent_result_list
        get_result_list()

        
        work(service, user_id, labels_map)

    except Exception as e: 
        print(e)
    
    