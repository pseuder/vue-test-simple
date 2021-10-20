#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# use : python==3.6.3
# pip install -r requirement.txt
# put file ".credentials" in ~/ 
# modify expiring/expired days in "variable.py"

import os, sys, httplib2
import json, shutil, sqlite3, datetime


import send_email
import variable

license_db_path = os.path.join(os.getcwd(), 'public', 'static',variable.license_DB)
notice_folder_path = os.path.join(os.getcwd(),'notice')
today = datetime.date.today()
today_folder_path = os.path.join(notice_folder_path,str(today))
expiring_folder_path = os.path.join(today_folder_path,'expiring')
expired_folder_path = os.path.join(today_folder_path,'expired')
# 取得即將到期通知天數
expiring_notice_date = variable.expiring_soon_date
# 取得已經到期通知天數
expired_notice_date = variable.expired_date


def unexpected_DB_close(func):
    # 當license DB發生非預期情況時關閉連線
    def warp(*args):
        try:
            return func(*args)
        except Exception as e:
            print(e)
            args[0].get('connection').close()
    return warp


def Connect_spl():
    # 連接license_DB
    global license_db_path
    if os.path.exists(license_db_path):
        try:
            conn = sqlite3.connect(license_db_path)
            conn.text_factory = str
            c = conn.cursor()
            return conn, c
        except Exception as e:
            return e
    else:
        print(' *SQLite : Can\'t find '+license_db_path+' !')
        return 'Can\'t find '+license_db_path



@unexpected_DB_close
def get_notice_expires_emails(args):
    # 群組 notice_expires，收到所有資料
    notice_expires_emails = []
    local_cursor = args.get('cursor')
    local_cursor.execute(f"SELECT members FROM groups WHERE name='notice_expires'")
    notice_expires_group = local_cursor.fetchone()[0]
    if notice_expires_group == '':
        notice_expires_group = []
    else:
        notice_expires_group = eval(notice_expires_group)
    
    for n_id in notice_expires_group:
        local_cursor.execute(f"SELECT email FROM users WHERE id='{n_id}'")
        n_email = local_cursor.fetchone()[0]
        notice_expires_emails.append(n_email)
    
    return notice_expires_emails

@unexpected_DB_close
def get_mapping(args):
    c = args.get('cursor')

    # 取得region對應
    region_map = {}
    cursor = c.execute('SELECT id, name FROM region')
    for row in cursor:
        region_map [str(row[0])] = str(row[1])

    # 取得product對應
    product_map = {}
    cursor = c.execute('SELECT category_id, product_name, caption FROM products')
    for row in cursor:
        product_map [row[1]] = {'category_id':row[0], 'caption': row[2]}
    
    # 取得option對應
    option_map = {}
    cursor = c.execute('SELECT product_name, option_name, caption FROM options')
    for row in cursor:
        option_map [row[1]] = {'product_name':row[0], 'caption': row[2]}

    # 取得module對應
    module_map = {}
    cursor = c.execute('SELECT mod_uid, caption FROM modules')
    for row in cursor:
        module_map [row[0]] = row[1]
    return region_map, product_map, option_map, module_map

def tr_html_table(cvs_file):
    try:
        modify_data = '<table border="1" text-align:center>'
        a = open(cvs_file,'r', encoding="utf-8")
        for line in a:
            if ('.0' in line):
                line = line.replace('.0','')
            if (',*' in line):
                line = line.replace(',*','</td><td style="background-color:#fff063">')
            if (',%*' in line):
                line = line.replace(',%*','</td><td style="color: red">')
            if (',' in line):
                line = line.replace(',','</td><td>')
            modify_data = modify_data +'<tr><td>' + line +'</td>'
        modify_data = modify_data+'</table>'
    except Exception as e:
        print('in tr_html_table :'+str(e))
        modify_data = None
    return modify_data

def count_day(count_date, mode):
    global today
    global expiring_notice_date
    global expired_notice_date
    notice_day_count = []
    if mode == 'expiring':
        notice_day_count = expiring_notice_date.split(';')
    elif mode == 'expired':
        notice_day_count = expired_notice_date.split(';')
    count = None
    year = int(count_date.split('-')[0])
    month = int(count_date.split('-')[1])
    day = int(count_date.split('-')[2])
    other_day = datetime.date(year,month,day)
    count = (other_day - today).days
    #Expiring soon
    if mode == 'expiring':
        if count >= 0:
            if (str(count) in notice_day_count) == False:
                count = None
        else: 
            count = None
    #Expired
    elif mode == 'expired':
        if count < 0:
            if (str(abs(count)) in notice_day_count) == False:
                count = None
        else: 
            count = None
    return count

@unexpected_DB_close
def sn_table_data(args):
    global region_map
    id = ''
    region = ''
    SN = args.get('sn')
    conn, c = args.get('connection'), args.get('cursor')
    cursor = c.execute('''SELECT id, region FROM sn WHERE sn=?''', (SN,))
    for row in cursor:
        id = row[0]
        region = region_map.get(row[1])
        if region == None:
            region = row[1]
    return id, region

@unexpected_DB_close
def customers_table_data(args):
    customer = ''
    name = ''
    site = ''
    customer_id = args.get('id')
    conn, c = args.get('connection'), args.get('cursor')
    cursor = c.execute('''SELECT name, site FROM customers WHERE id=?''', (customer_id,))
    for row in cursor:
        name = row[0]
        site = row[1]
    if site == '':
        customer = name
    else:
        customer = name+'|'+site
    return customer

def output_expiration_cvs(whos, data, mode):
    Title = "客戶,Key ID,到期日,產品名稱,類型,數量,地區,備註,連絡人\n"
    contact_list = []
    data = data+"\n"
    global expiring_folder_path
    global expired_folder_path
    global notice_expires_emails
    if whos :
        if ';' in whos :
            contact_list = whos.split(';')
        elif '；' in whos :
            contact_list = whos.split('；')
        elif whos != '':
            contact_list.append(whos)
    for notice_expires in notice_expires_emails:
        if notice_expires not in contact_list:
            contact_list.append(notice_expires)
    
    if mode == 'expiring':
        expi_path = expiring_folder_path
    elif mode == 'expired':
        expi_path = expired_folder_path

    for contact in contact_list:
        contact = contact.replace(' ','')
        contact_txt = os.path.join(expi_path,contact)
        if not os.path.exists(contact_txt):
            with open(contact_txt, 'a', encoding="utf-8") as f:
                f.write(Title)
                f.write(data)
                f.close()
        else:
            no_duplicate  = True
            data_slot = data.split(',')
            with open(contact_txt, 'r', encoding="utf-8") as f:
                for line in f.readlines():
                    line_slot = line.split(',')
                    # 過濾相同客戶+SN+產品
                    if((data_slot[1] == line_slot[1]) and  (data_slot[2] == line_slot[2]) 
                        and (data_slot[3] == line_slot[3])):
                        no_duplicate = False
            if no_duplicate:
                with open(contact_txt, 'a', encoding="utf-8") as f:
                    f.write(data)
                    f.close()
    return contact_txt

def mail_expiration(mode):
    global expiring_folder_path
    global expired_folder_path
    global today
    global expiring_notice_date
    global expired_notice_date
    recipient = []
    if mode == 'expiring':
        recipient = os.listdir(expiring_folder_path)
    elif mode == 'expired':
        recipient = os.listdir(expired_folder_path)
    if len(recipient) > 0:
        for to in recipient:
            if mode == 'expiring':
                msgHtml_file = os.path.join(expiring_folder_path,to)
                msgHtml = tr_html_table(msgHtml_file)
                msgHtml = f"License 即將到期，如 USB Key已收回，請協助刪除 \
                            登入網址: https://{variable.app_name}.herokuapp.com <br> \
                            通知頻率(到期前天數): {expiring_notice_date} <br>" + msgHtml

                send_email.SendMessage(to, '', variable.expiring_title + str(today), msgHtml)
            elif mode == 'expired':
                msgHtml_file = os.path.join(expired_folder_path,to)
                msgHtml = tr_html_table(msgHtml_file)
                msgHtml = f"License 已經到期，如 USB Key已收回，請協助刪除 \
                            登入網址: https://{variable.app_name}.herokuapp.com <br> \
                            通知頻率(過期後天數): {expired_notice_date} <br>" + msgHtml

                send_email.SendMessage(to, '', variable.expired_title + str(today), msgHtml)
    return

def get_product_name(func_uid):
    # 如func_uid不存在，則直接顯示
    global product_map
    global option_map
    if option_map.get(func_uid):
        product_name = option_map.get(func_uid).get('product_name')
        if product_map.get(product_name):
            return product_map.get(product_name).get('caption')
        else:
            return product_name
    elif product_map.get(func_uid):
        return product_map.get(func_uid).get('caption')
    else:
        return func_uid


@unexpected_DB_close
def check_expiration(argc):
    global expiring_folder_path
    global expired_folder_path
    global module_map

    mode = argc.get('mode')
    # 清除之前儲存的資料
    if mode == 'expiring':
        if os.path.isdir(expiring_folder_path):
            shutil.rmtree(expiring_folder_path)
            os.mkdir(expiring_folder_path)
        else:
            os.mkdir(expiring_folder_path)
    elif mode == 'expired':
        if os.path.isdir(expired_folder_path):
            shutil.rmtree(expired_folder_path)
            os.mkdir(expired_folder_path)
        else:
            os.mkdir(expired_folder_path)


    remind = None
    conn, c = argc.get('connection'), argc.get('cursor')
    cursor = c.execute('''SELECT sn, func_uid, issued, expiration, count, \
                        registration, type, comment, contact FROM info''')
    for row in cursor:
        sn = row[0]
        func_uid = row[1]
        issued = row[2]
        expiration = row[3]
        count = row[4]
        registration = row[5]
        type = row[6]
        comment = row[7]
        contact = row[8]
        remind = count_day(expiration, mode)
        if remind != None :
            id, region = sn_table_data({'connection': conn, 'cursor': c, 'sn': sn})
            customers = customers_table_data({'connection': conn, 'cursor': c, 'id': id})
            product_name = get_product_name(func_uid)
            type = module_map.get(type)
            if mode == 'expiring':
                expires_Message = customers+','+str(sn)+',*'+expiration+','+product_name+','+\
                        type+','+str(count)+','+region+','+str(comment)+','+str(contact)
            elif mode == 'expired':
                expires_Message = customers+','+str(sn)+',%*'+expiration+','+product_name+','+\
                        type+','+str(count)+','+region+','+str(comment)+','+str(contact)
            output_expiration_cvs(contact, expires_Message, mode)
    mail_expiration(mode)
    return



if __name__ == '__main__':
    # 存放於notice資料存
    if not os.path.isdir(notice_folder_path):
        os.mkdir(notice_folder_path)
    if not os.path.isdir(today_folder_path):
        os.mkdir(today_folder_path)

    # 取得notice_expires群組(連接完整DB)
    local_database = sqlite3.connect("db.sqlite3")
    local_cursor = local_database.cursor()
    notice_expires_emails = get_notice_expires_emails({'connection': local_database, 'cursor': local_cursor})
    local_database.close()

    # 連接licenseDB
    license_database, license_cursor = Connect_spl()
    region_map, product_map, option_map, module_map = get_mapping({'connection': license_database, 'cursor': license_cursor})
    # 即將到期
    check_expiration({'connection': license_database, 'cursor': license_cursor, 'mode': 'expiring'})
    # 已經過期
    check_expiration({'connection': license_database, 'cursor': license_cursor, 'mode': 'expired'})
    license_database.close()