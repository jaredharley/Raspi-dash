#!/usr/bin/python

import os
import socket

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 0))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def get_temperature(scale = "c"):
    with open('/sys/class/thermal/thermal_zone0/temp') as f:
        tempfile = list(f)
    if len(tempfile) > 0:
        temp = float(tempfile[0])
        temp = temp/1000
        if scale == "f":
            return temp*1.8+32
        else:
            return temp

def get_uptime_string():
    with open('/proc/uptime') as f:
        lines = list(f)
    if len(lines) <= 0:
        return "Unable to determine uptime"
    uptime = lines[0].split()
    uptime = float(uptime[0])
    m, s = divmod(uptime, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    return "%d days, %d hours, %02d minutes, %02d seconds" % (d,h,m,s)

def main():
    uname = os.uname()
    
    print("Raspberry Pi status")
    print("===================")
    print("Host name: " + uname[1])
    print("IP address: " + get_ip())
    print(uname[0] + " " + uname[2] + " " + uname[4])
    print("Temperature: " + str(get_temperature("f")) + " degrees F") 
    print("Uptime: " + get_uptime_string())

if __name__ == "__main__":
    main()
