import os
import socket
import subprocess
from datetime import datetime
import time

class Stats():

    def get_memory():
        """Returns memory statistics from /proc/meminfo as a dict
        Dict keys:
        total    - Total memory
        free     - Free memory
        used     - Used memory (total minus free)
        buffer   - Buffered memory
        cache    - Cached memory
        usedless - Used memory with buffered and cached memory removed
        """
        with open('/proc/meminfo') as f:
            memfile = list(f)
        if len(memfile) <= 0:
            return "Unable to get memory info"
        memtotal = float((memfile[0].split())[1])
        memfree  = float((memfile[1].split())[1])
        memused  = memtotal - memfree
        membuffers = float((memfile[3].split())[1])
        memcache = float((memfile[4].split())[1])
        memusedless = memused - membuffers - memcache
        return {'total':memtotal,'free':memfree,'used':memused,'buffer':membuffers,'cache':memcache,'usedless':memusedless}

    def get_ip_address():
        """Returns the ip address."""
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

    def get_temperature(scale='c'):
        """Returns the temperature of the board from /sys/class/thermal/thermal_zone0/temp
        as a float rounded to 2 decimal places (or -1 if the temp couldn't be read).
        
        Keyword arguments:
        scale -- temperature scale (f or c). Default: 'c'.
        """
        with open('/sys/class/thermal/thermal_zone0/temp') as f:
            tempfile = list(f)
        if len(tempfile) > 0:
            temp = float(tempfile[0])
            temp = temp/1000
            if scale == "f":
                return round(temp*1.8+32,2)
            else:
                return round(temp,2)

    def get_uptime():
        """Returns the uptime from /proc/uptime as a dict object.
        Dict values:
        days, hours, minutes, seconds
        """
        with open('/proc/uptime') as f:
            lines = list(f)
        if len(lines) <= 0:
            return "Unable to determine uptime"
        uptime = lines[0].split()
        uptime = float(uptime[0])
        m, s = divmod(uptime, 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)
        return {'days':d,'hours':h,'minutes':m,'seconds':s}

    def get_last_boot():
        """Retuns a datetime object of the last boot time from the command
        who -b."""
        lastboot = subprocess.check_output(['who','-b'])
        if len(lastboot) <= 0:
            return
        lastboot = lastboot.split()
        if len(lastboot) != 4:
            return
        lbdate = datetime.strptime(lastboot[2]+","+lastboot[3], "%Y-%m-%d,%H:%M")
        return lbdate

    def get_filesystem():
        """Returns each row of the df -h output as a string in a list."""
        fs = subprocess.check_output(['df','-h'])
        if len(fs) <= 0:
            return
        fs = fs.split('\n')
        return fs

    def get_cpu():
        """Returns a dict with the one, five, and fifteen minute load
        averages from uptime.
        Dict values:
        onemin, fivemin, fifteenmin"""
        uptime = subprocess.check_output(['uptime'])
        if len(uptime) <= 0:
            return
        try:
            la = uptime.split('load average:')[1]
        except IndexError:
            return
        
        avg = la.split(',')
        if len(avg) != 3:
            return
    
        return {'onemin':float(avg[0]),'fivemin':float(avg[1]),'fifteenmin':float(avg[2])}

    def get_network():
        """Returns a dict with the up and down traffic as bytes per second."""
        path = '/sys/class/net/eth0/statistics/'
        with open(path+'rx_bytes') as rx:
            rx1 = list(rx)
            rx1 = float(rx1[0])
        with open(path+'tx_bytes') as tx:
            tx1 = list(tx)
            tx1 = float(tx1[0])
        time.sleep(1)
        with open(path+'rx_bytes') as rx:
            rx2 = list(rx)
            rx2 = float(rx2[0])
        with open(path+'tx_bytes') as tx:
            tx2 = list(tx)
            tx2 = float(tx2[0])
    
        stats = [rx2-rx1,tx2-tx1]
        return {'down':stats[0],'up':stats[1]}

    ip_address = get_ip_address()
    memory = get_memory()
    temp_f = get_temperature('f')
    temp_c = get_temperature('c')
    raw_uptime = get_uptime()
    uptime = "%dd %dh %0dm" % (raw_uptime['days'], raw_uptime['hours'], raw_uptime['minutes'])
    last_boot = get_last_boot()
    filesystem = get_filesystem()
    cpu = get_cpu()
    network = get_network()
    name = os.uname()
