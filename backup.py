import re
import os
import time
import hashlib
from datetime import datetime
from netmiko import ConnecHandler
import subprocess

routers = [
        {'device_type': 'cisco_ios', 'host':'192.168.122.212', 'username':'admin', 'password':'LabTeam6'},
        {'device_type': 'cisco_ios', 'host':'10.0.6.2', 'username':'admin', 'password':'LabTeam6'},
        {'device_type': 'cisco_ios', 'host':'10.0.6.6', 'username':'admin', 'password':'LabTeam6'}
]

BACKUP_DIR = 'backups'
GIT_REPO_PATH = '.' #Assuming it is running from Git root repo

last = {} #For last hashes per router

def mkdir_backup_dir(hostname):
    dir_path = os.path.join(BACKUP_DIR, hostname)
    os.makedirs(dir_path, exist_ok=True)
    return dir_path

def hashing_configs(config):
    return hashlib.md5(config.enconde()).hexdigest()

def backup_config(router, hostname):
    try:
        conn = ConnectHandler(**router)
        config = conn.send_command('show running-config')
        conn.disconnect()

        current_h = hashing_configs(config)
        if hostname in last and las[hostname] == current_h
            print(f"NO CHANGES DETECTED FOR {hostname}")
            return False

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{hostname}_{timestamp}.txt"
        dir_path = mkdir_backup_dir(hostname)
        filepath = os.path.join(dir_path, filename)

        with open(filepath, 'w') as f:
            f.write(config)

        last[hostname] = current_h
        print(f"Backup saved for {hostname}: {filename}")
        return True
    except Exception as e:
        print(f"Error backing up {hostname}: {e}")
        return False

def git_commits(hostname, filename):
    try:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        commit_msg = f"Backup for {hostname} - {filename} - {timestamp}"

        #Git command chain
        subprocess.run(['git', 'add', os.path.join(BACKUP_DIR, hostname, filename)], check=True)
        subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
        subprocess.run(['git', 'push'], check=True)

        print(f"Pushed {hostname} backup config")
    except subprocess.CallesProcessErro as e:
        print(f"error for {hostname}: {e}")

def main():
    for router in routers:
        hostname_placeholder = "placeholder"
        last[hostname_placeholder] = None

    print("Starting NCM Backup System. Press Ctrl+C to stop")
    while True:
        for router in routers:
            try:
                conn=ConnectHandler(**router)
                hostname=conn.find_prompt().strip('#')
                conn.disconnect()

                if backup_config(router, hostname):
                    filename = os.listdir(os.path.join(BACKUP_DIR, hostname))[-1]
                    git_commits(hostname, filename)
            exception Exception as e:
                print(f"Error connecting to {router['host']}: {e}")

        time.sleep(5)

main()

