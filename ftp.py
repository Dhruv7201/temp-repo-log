from ftplib import FTP
from datetime import datetime


def upload_file_to_ftp(hostname, username, password, local_file_path, remote_file_path):
    ftp = FTP(hostname, username, password)
    ftp.set_pasv(False)
    with open(local_file_path, "rb") as file:
        ftp.storbinary(f"STOR {remote_file_path}", file)
    ftp.close()


# Example usage:
hostname = ""
username = ""

password = ""
local_file_path = f'/var/prod/log/{datetime.now().strftime("%Y-%m-%d")}_log.txt'
remote_file_path = f'VPoint_2/Mcode_102/{datetime.now().strftime("%Y-%m-%d")}_log.txt'

upload_file_to_ftp(hostname, username, password, local_file_path, remote_file_path)
