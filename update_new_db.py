# -*- coding: utf-8 -*- 
#將database資料寫入csv檔案中
import sys
import csv
import sqlite3
import codecs
import os
from datetime import datetime, timedelta, timezone

def write_csv_from_new_db(new_db):
    database = sqlite3.connect(new_db)
    cursor = database.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    local_Tables = cursor.fetchall()

    tables = []
    for table in local_Tables:
        tables.append(table[0])

    if not os.path.isdir("./csv"):
        os.mkdir("./csv")

    for table in tables:
        csv_file = codecs.open(('./csv/%s.csv') % table, 'w', encoding='utf-8')
        writer = csv.writer(csv_file)

        for row in cursor.execute("SELECT * FROM %s" % table):
            writer.writerow(row)

        csv_file.close()
    print("CSV write done")

def write_localDB_from_csv():
    os.system(f'python write_model_from_csv.py -nonempty')
    print("local DB write done")

def push_heroku(new_db):
    i = datetime.now()
    i = i.astimezone(timezone(timedelta(hours=8)))#台灣時區GMT+8
    update_time = (("%d/%02d/%02d %02d:%02d:%02d") % (i.year, i.month, i.day, i.hour, i.minute, i.second))
    os.system(f'git add .')
    os.system(f'git commit -m "update new DB:{new_db} at {update_time}"')
    os.system(f'git push')
    print("Heroku push done")

def write_webDB_from_csv():
    os.system(f'heroku run python write_model_from_csv.py -nonempty')
    print("Heroku update done")

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("*---Warning!---*\nPlease input new DB name after update_new_db.py")
        sys.exit(1)

    if not os.path.exists(sys.argv[1]):
        print(f"*---Error!---*\nCan't find new DB {sys.argv[1]}")
        sys.exit(1)


    new_db = sys.argv[1]
    write_csv_from_new_db(new_db)
    if new_db != 'db.sqlite3':
        write_localDB_from_csv()
    push_heroku(new_db)
    write_webDB_from_csv()