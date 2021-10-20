#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# use : python==3.6.3rc1

import os
import json
import csv
import time
import sqlite3

from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase #用於承載附檔
from email import encoders #用於附檔編碼
from email.mime.text import MIMEText
import base64

from license_server import update_localDB_from_postgresql, update_licenseDB_from_localDB, create_license, push_heroku
import variable
from send_email import SendMessage


DIR = os.path.abspath('.')
Verifier_email = 'claire@eastek.com.tw'

class Auto_Extension():
    # 將隔年到期日為xxxx-01-31的資料，自動往後延期1年，產出license並寄信
    def __init__(self): 
        # variables
        self.application_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.today = time.strftime("%Y-%m-%d", time.localtime())

        # path
        self.DIR = os.path.abspath('.')
        self.db_path = os.path.join(self.DIR, 'db.sqlite3')
        self.license_folder = os.path.join(self.DIR, 'public', 'static')
        self.license_path = os.path.join(self.license_folder, 'license')
        self.license_DB_path = os.path.join(self.license_folder, variable.license_DB)
        self.csv_folder = os.path.join(self.DIR, 'extension', self.today)   #紀錄

        # condition
        self.filter_customers_list = ['eastek']
        # 符合自動延期的日期
        year = str(int(time.strftime("%Y", time.localtime()))+1)
        self.expiry_date = year + '-01-31'

        # 往後延一年的日期
        year = str(int(time.strftime("%Y", time.localtime()))+2)
        self.expiry_next_date = year + '-01-31'
        
        # 符合自動延期的id
        self.auto_extension_info_id = []

        update_localDB_from_postgresql()

        self.main()

    def Connect_spl(self):
        if os.path.exists(self.db_path):
            try:
                conn = sqlite3.connect(self.db_path)
                conn.text_factory = str
                c = conn.cursor()
                return conn, c
            except Exception as e:
                return e
        else:
            print(' *SQLite : Can\'t find '+self.db_path+' !')
            return 'Can\'t find '+self.db_path

    def transform_modules(self, db_path, type, word):
        conn, c = self.Connect_spl()
        info_tuple = (word,)
        transform_word = None
        mod_uid = None
        caption = None
        try:
            if ((type == 'caption') or (type == 'mod_uid')):
                if type == 'caption':
                    c.execute("SELECT * FROM modules WHERE caption=? ",info_tuple)
                elif type == 'mod_uid':
                    c.execute("SELECT * FROM modules WHERE mod_uid=? ",info_tuple)
                cursor = c.fetchall()
                data_exist = len(cursor)
                #print '   translate : '+type+','+word+', exist : '+str(data_exist)
                if data_exist < 1: # data_exist = 0 -> 沒
                    transform_word = 'error database has no data : '+word
                else:
                    for row in cursor:
                        #print row
                        mod_uid = row[0]
                        caption = row[1]
                        break
                    if type == 'caption':
                        transform_word = mod_uid
                    elif type == 'mod_uid':
                        transform_word = caption
            else:
                transform_word = 'type text error'
        except Exception as e:
            print('transform_modules line53 '+str(e))
            return e
        conn.close()
        return transform_word

    def transform_region(self, type, word):
        conn, c = self.Connect_spl()
        info_tuple = (word,)
        transform_word = None
        id = None
        name = None
        try:
            if ((type == 'id') or (type == 'name')):
                if type == 'id':
                    c.execute("SELECT * FROM region WHERE id=? ",info_tuple)
                elif type == 'name':
                    c.execute("SELECT * FROM region WHERE name=? ",info_tuple)
                cursor = c.fetchall()
                data_exist = len(cursor)
                if data_exist < 1: # data_exist = 0 -> 沒
                    transform_word = 'error database has no data : '+word
                else:
                    for row in cursor:
                        id = row[0]
                        name = row[1]
                        break
                    if type == 'name':
                        transform_word = id
                    elif type == 'id':
                        transform_word = name
            else:
                transform_word = 'type text error'
        except Exception as e:
            print('transform_modules'+str(e))
            return e
        conn.close()
        return transform_word

    def tr_html_table(self, csv_file):
        try:
            modify_data = '<body><table border="1" text-align:center>'
            a = open(csv_file,'r', encoding="utf-8")
            for line in a:
                if ('.0' in line):
                    line = line.replace('.0','')
                if (',*' in line):
                    line = line.replace(',*','</td><td style="background-color:#98FB98">')
                if (',' in line):
                    line = line.replace(',','</td><td>')
                modify_data = modify_data +'<tr><td>' + line +'</td>'
            modify_data = modify_data+'</table></body>'
        except Exception as e:
            print('in tr_html_table :'+str(e))
            modify_data = None
        return modify_data

    def sn_table_data(self, SN):
        id = ''
        region = ''
        conn, c = self.Connect_spl()
        cursor = c.execute('''SELECT id, region FROM sn WHERE sn=?''', (SN,))
        for row in cursor:
            id = row[0]
            region = row[1]
        region = self.transform_region('id', region)
        conn.close()
        return id, region

    def customers_table_data(self, customer_id):
        customer = ''
        name = ''
        site = ''
        conn, c = self.Connect_spl()
        cursor = c.execute('''SELECT name, site FROM customers WHERE id=?''', (customer_id,))
        for row in cursor:
            name = row[0]
            site = row[1]
        if site == '':
            customer = name
        else:
            customer = name+'|'+site
        conn.close()
        return customer

    def output_extension_csv(self, whos, data):
        Title = "客戶,申請日期,產品編號/ID號碼(sn),產品名稱,類型,數量(USER),使用期限,地區,備註,連絡人\n"
        contact_list = []
        data = data+"\n"
        if whos :
            if ';' in whos :
                contact_list = whos.split(';')
            elif '；' in whos :
                contact_list = whos.split('；')
            elif whos != '':
                contact_list.append(whos)
        if Verifier_email not in contact_list:
            contact_list.append(Verifier_email)
        for contact in contact_list:
            contact = contact.replace(' ','')
            contact_txt = os.path.join(self.csv_folder,contact)
            if not os.path.exists(contact_txt):
                with open(contact_txt, 'a', encoding="utf-8") as f:
                    f.write(Title)
                    f.write(data)
                    f.close()
            else:
                with open(contact_txt, 'a', encoding="utf-8") as f:
                    f.write(data)
                    f.close()
        return 

    
    def modify_database(self):
        conn, c = self.Connect_spl()
        for id in self.auto_extension_info_id:
            c.execute("UPDATE info set issued=?, expiration=? WHERE id=?",
                (self.today, self.expiry_next_date, id))
        conn.commit()
        conn.close()

    def mail_extension(self):
        recipient = os.listdir(self.csv_folder)
        if len(recipient) > 0:
            for to in recipient:
                csv_to_path = os.path.join(self.csv_folder,to)

                msg = MIMEMultipart('mixed')
                msg['From'] = variable.Sender_email_account
                # msg['To'] = to
                # msg['To'] = 'claire@eastek.com.tw'   #test
                msg['To'] = 'iop890520@gmail.com'   #test
                msg['Subject'] =  f'{variable.auto_expiration_title}'

                # 夾帶license
                with open(self.license_DB_path, 'rb') as fp:
                    add_file = MIMEBase('application', "octet-stream")
                    add_file.set_payload(fp.read())
                    encoders.encode_base64(add_file)
                    add_file.add_header('Content-Disposition', 'attachment', filename='license')
                    msg.attach(add_file)

                
                msg.attach(MIMEText(self.tr_html_table(csv_to_path), 'html'))
                encodeMsg = {'raw': (base64.urlsafe_b64encode(msg.as_bytes())).decode("utf-8") }
                result = SendMessage('', '', '', '', encodeMsg)
                if result == 'error':
                    print("mail_extension fail!")
                    return
            print('mail_extension done')
         

    def main(self):
        print('========== '+self.today+' ==========')
        print('expiry date : '+self.expiry_date)
        print('filter customers : '+str(self.filter_customers_list))
        if not os.path.isdir(os.path.join(self.DIR,'extension')):
            os.mkdir(os.path.join(self.DIR,'extension'))
        if not os.path.isdir(self.csv_folder):
            os.mkdir(self.csv_folder)
        conn, c = self.Connect_spl()
        cursor = c.execute('''SELECT sn, func_uid, issued, expiration, count, \
                            registration, type, comment, contact, id FROM info''')

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
            info_id = row[9]
            if ((type == 'OFFICIAL') and (contact) and (expiration == self.expiry_date)):
                id, region = self.sn_table_data(sn)
                customers = self.customers_table_data(id)
                func_uid = self.transform_modules(self.db_path, 'mod_uid', func_uid)
                type = self.transform_modules(self.db_path, 'mod_uid', type)
                if (customers not in self.filter_customers_list):
                    extension_Message = customers+','+issued+','+str(sn)+','+func_uid+','+\
                        type+','+str(count)+',*'+self.expiry_next_date+','+region+','+str(comment)+','+str(contact)
                    self.output_extension_csv(contact, extension_Message)
                    self.auto_extension_info_id.append(info_id)
        conn.close()

        print('  Modify DB......')
        status = self.modify_database()

        print('  Update license DB......')
        update_licenseDB_from_localDB()

        print('  Create license ......')
        # create_license參數: db_path, target_path)
        create_license(self.license_DB_path, self.license_path)

        print('  Mail license ......')
        self.mail_extension()

        print('  Update license web ......')
        push_heroku()
        
        print('Done')


if __name__ == '__main__':
    Auto_Extension()
