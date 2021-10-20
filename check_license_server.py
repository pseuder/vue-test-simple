import psutil
import os

def run_license_server():
    os.system('python license_server.py')

pid = 0

target_path = os.getcwd() + '\\license_server.pid'

if os.path.isfile(target_path):
    with open('license_server.pid', 'r') as f:
        pid = int(f.read())
    if(psutil.pid_exists(pid)):
        myprocess = psutil.Process(pid)
        if myprocess.name() != 'python.exe':
            run_license_server()
    else:
        run_license_server()
else:
    run_license_server()





              