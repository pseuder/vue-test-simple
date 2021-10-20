#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import shutil
import time

# moudule
import variable

def clone_Bitbucket(path, repo):
    URL = f'https://{variable.bitbucket_user}:{variable.bitbucket_pwd}@bitbucket.org/{variable.bitbucket_team}/{repo}.git'
    os.system(f'git clone {URL}')
    return

def pull_Bitbucket(repo_path, branch):
    os.chdir(repo_path)
    os.system(f'git pull origin {branch}')
    return

def push_Bitbucket(repo_path, msg, branch):
    os.chdir(repo_path)
    os.system('git add .')
    os.system(f'git commit -m {msg}')
    os.system(f'git push origin {branch}')
    return

def update(current_path, db_path, license_path):
    """ 將最新的 DB、License 更新到對應的倉庫 """
    repo_dir = os.path.join(current_path, "update_repo")
    branch = 'master'
    commit_time = time.strftime("%Y%m%d_%H%M", time.localtime())
    msg = 'License Request server update time : '+commit_time
    if not os.path.exists(repo_dir):
        os.mkdir(repo_dir)
    
    # update database
    repo_path = os.path.join(repo_dir, variable.bitbucket_db_repo)
    if not os.path.exists(repo_path):
        clone_Bitbucket(repo_path, variable.bitbucket_db_repo)
    else:
        pull_Bitbucket(repo_path, branch)
    
    if not os.path.exists(os.path.join(repo_path, "CustomerInfoDBv2")):
        os.mkdir(os.path.join(repo_path, "CustomerInfoDBv2"))
    db_path_des = os.path.join(repo_path, "CustomerInfoDBv2", variable.license_DB)
    shutil.copyfile(db_path, db_path_des)
    push_Bitbucket(repo_path, msg, branch)

    # update license
    repo_path = os.path.join(repo_dir, variable.bitbucket_license_repo)
    if not os.path.exists(repo_path):
        clone_Bitbucket(repo_path, variable.bitbucket_license_repo)
    else:
        pull_Bitbucket(repo_path, branch)
    
    license_path_des = os.path.join(repo_path, 'share','license','license')
    shutil.copyfile(license_path, license_path_des)
    push_Bitbucket(repo_path, msg, branch)

    return 

if __name__ == '__main__':
    current_path = os.getcwd()
    db_path = f'{current_path}/public/static/{variable.license_DB}'
    license_path = f'{current_path}/public/static/license'
    update(current_path, db_path, license_path)
