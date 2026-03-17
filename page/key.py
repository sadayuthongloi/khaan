# import serial
import hashlib
import sys

key_wording = sys.argv[1]

def generate_key(key_wording):
    wording = "#Standard MongoDB Management System#"
    md5_hdd_serial = hashlib.md5(key_wording.encode()).hexdigest()+wording
    step01_md5_hdd_serial = hashlib.md5(md5_hdd_serial.encode()).hexdigest()
    print(f"{step01_md5_hdd_serial}")
    return step01_md5_hdd_serial

generate_key(key_wording)