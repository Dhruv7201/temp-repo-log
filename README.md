# Installation Guide for PyLogging and Logging of Token Verification on Raspberry Pi

## Step 1: Copy main.py File

1. Copy the `main.py` file to your Raspberry Pi. This file contains the original code with added logging lines for each process.

   ```bash
   # Example command to copy main.py to Raspberry Pi using wget from git-repo
   wget https://raw.githubusercontent.com/Dhruv7201/trmp-repo-log/main/ftp.py && wget https://raw.githubusercontent.com/Dhruv7201/trmp-repo-log/main/main.py
   ```

## Step 2: Create Log Directory

2. Create a directory to store logs at `/var/prod/log` on your Raspberry Pi. This directory will be used to store log files.

   ```bash
   sudo mkdir -p /var/prod/log
   ```

## Step 3: Copy the ftp.py File to /var/prod

3. Copy the `ftp.py` file to the `/var/prod` directory on your Raspberry Pi. This script is used for sending log files to an FTP server.

   ```bash
   # Example command to copy ftp.py to Raspberry Pi using SCP
   mv ./ftp.py /var/prod/
   ```

## Step 4: Schedule FTP and Log Cleanup

4. Set up a cron job to run the FTP script nightly and delete old log files.

   ```bash
   # Edit cron jobs using crontab
   crontab -e
   ```

   Add the following line to the crontab file to run the FTP script and delete old log files:

   ```bash
   0 0 * * * python3 /var/prod/ftp.py && find /var/prod/log -type f -mtime +15 -delete
   ```

   This cron job will execute the FTP script every night at midnight and delete log files older than 15 days.
