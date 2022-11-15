import time

from pythonping import ping
import pycurl
import certifi
from io import BytesIO

#Alle Ports, die der Switch haben kann
port_all = [1, 2, 3, 4, 5, 6, 7, 8]

#Port, an dem der Computer hängt
port_computer = 1

#Ports, wo der Controller dran hängen kann
port_list = [2, 3, 4]

pingable_controller_ip = "192.168.0.11"


def port_enable(port):
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, f'http://192.168.0.254/php/command.php?usr=admin&pwd=private&cmd=port%20{port}%20admin-mode%20enable')
    c.setopt(c.WRITEDATA, buffer)
    c.setopt(c.CAINFO, certifi.where())
    c.perform()
    c.close()
    body = buffer.getvalue()
    print(body.decode('iso-8859-1'))

def port_disable(port):
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, f'http://192.168.0.254/php/command.php?usr=admin&pwd=private&cmd=port%20{port}%20admin-mode%20disable')
    c.setopt(c.WRITEDATA, buffer)
    c.setopt(c.CAINFO, certifi.where())
    c.perform()
    c.close()
    body = buffer.getvalue()
    print(body.decode('iso-8859-1'))

def port_disable_all(port_all, port_computer):
    #geht alle Ports am Switch durch
    for i in port_all:
        #Wenn der durchgegangene Port nicht der Computerport ist
        if i != port_computer:
            port_disable(i)

#setzt allen Controller Test Ports eine gewünschte Ip-Adresse zum Pingen (Funktioniert nur ohne Controller anschluss)
def port_set_ip(i, new_ip):
    command = f'http://192.168.0.254/php/command.php?usr=admin&pwd=private&cmd=dhcp-service%20server%20port-local-clear%20|%20dhcp-service%20server%20port-local%20{i}%20status%20enable%20|%20dhcp-service%20server%20port-local%20{i}%20net-mask%20255.255.255.000%20|%20dhcp-service%20server%20port-local%20{i}%20local-ip%20{new_ip}'
    print(command)
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, command)
    c.setopt(c.WRITEDATA, buffer)
    c.setopt(c.CAINFO, certifi.where())
    c.perform()
    c.close()
    body = buffer.getvalue()
    print(body.decode('iso-8859-1'))

def check_ping(ip, port):
    for i in range(3):
        time.sleep(30)
        print(f"{ip} on Port {port} - Ping: {i+1}")
        response = ping(ip, verbose=False)
        if response.success() == True:
            print(f"Port: {port}, erfolgreich")
            break
        elif i == 2: print(f"Port: {port}, nicht erfolgreich")

def port_test(port):
    port_set_ip(port, pingable_controller_ip)
    port_enable(port)
    check_ping(pingable_controller_ip, port)
    port_disable(port)

def start_testing(port_list):
    port_disable_all(port_all, port_computer)

    for port in port_list:
        port_test(port)

start_testing(port_list)

