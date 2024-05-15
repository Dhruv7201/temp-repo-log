from ftplib import FTP
from datetime import datetime

def upload_file_to_ftp(hostname, username, password, local_file_path, remote_file_path):
    ftp = FTP(hostname, username, password)
    ftp.ftp.set_pasv(False)
    with open(local_file_path, 'rb') as file:
        ftp.storbinary(f'STOR {remote_file_path}', file)
    ftp.close()

# Example usage:
hostname = '164.52.196.173'
username = 'tapovan'

password = 'Tapovan@2024'
local_file_path = f'/var/prod/log/{datetime.now().strftime("%Y-%m-%d")}_log.txt'
remote_file_path = f'Mcode_102/VPoint_2/{datetime.now().strftime("%Y-%m-%d")}_log.txt'

upload_file_to_ftp(hostname, username, password, local_file_path, remote_file_path)
