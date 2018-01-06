# ble-server
## Requirements:
 ### 1. Operating System:
  * Ubuntu Mate Xenial 16.04.3 LTS for Raspberry Pi (RPI 2, 3).
  * Other Linux distributions meeting requirements.  

 ### 2. Unix packages:
  * bluez >= 5.41
  * python >= 3.5.2
  * libglib2.0
 ### 3. Python modules:
  * bluepy >= 1.1.4
  * pony >= 0.7.3
  * flask>=0.12
  * mysqlclient>=1.3.12

## Running server:

python3 run.py <log_file> 

If setting LOGFILE is True then, server will save logs to automatically created 
file in /logs direcotry or to specified file if commandline parameter log_file.