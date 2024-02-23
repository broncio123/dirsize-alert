import os
import json
import time
import socket
import smtplib
import pathlib
import shutil
import subprocess
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email configuration
with open('alert_config.json','r') as f:
    config = json.load(f)

sender_email = config['sender_email']
receiver_email = config['receiver_email']
password = config['password']
target_dir = config['target_dir']

hostname = socket.gethostname()

def send_email_notification(directory, total_dir_size, threshold_kb):
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = f'Directory Size Alert: {hostname}'
    body = f"Warning: Directory '{directory}' size exceeded {threshold_kb} KB allowed limit.\nYour directory is currently {total_dir_size} KB in size."
    message.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.send_message(message)

def get_dir_diskspace(directory):
    p = subprocess.run(['du','-s',directory], stdout=subprocess.PIPE)
    diskspace_kb = int(p.stdout.decode().split('\t')[0]) # space reserved in disk
    return diskspace_kb

def run_test():
    parent_dir = pathlib.Path(__file__).parent.resolve()
    testdir = os.path.join(parent_dir, 'testdir')
    if not os.path.isdir(testdir):
        os.mkdir(testdir)
    else:
        print('INFO: testdir already exists.')

    # Create test files (~ 4.0 MB)
    N = 1000
    for i in range(N):
        filepath = os.path.join(testdir, f"hello{i}.txt")
        f = open(filepath, "w")
        f.write("Hello World!\n") # 4 KB in disk space
        f.close()

    diskspace_kb = get_dir_diskspace(testdir)
    print(f"INFO: Generated 1000 text files with a total disk space use of {diskspace_kb} KB")

    threshold_kb = 1000 # KB
    if diskspace_kb > threshold_kb:
        try:
            send_email_notification(testdir, diskspace_kb, threshold_kb)
            print("INFO: Sent test email notification!")
            success = True
        except Exception as e:
            print(f"ERROR: Test email failed. {e}")
    
    if success:
        print("INFO: Test was successful. Deleting 'testdir' and contents.")
        shutil.rmtree(testdir)

def check_directory_size(target_dir, threshold_kb = 500000000):
    diskspace_kb = get_dir_diskspace(target_dir)
    print(f"INFO: Your directory '{target_dir}' is currently using {diskspace_kb} KB in disk space.")

    if diskspace_kb > threshold_kb:
        try:
            send_email_notification(target_dir, diskspace_kb, threshold_kb)
            print("INFO: Sent test email notification!")
            success = True
        except Exception as e:
            print(f"ERROR: Test email failed. {e}")

if __name__ == "__main__":
    import sys
    test = sys.argv[1]
    if test.strip().lower() == 'y':
        run_test()
    else:
        # Limit of 500 GB
        threshold_kb = 500000000
        while True:
            check_directory_size(threshold_kb)
            n_hours = 24
            time_sleep = 60*60*n_hours # seconds
            time.sleep(time_sleep)
