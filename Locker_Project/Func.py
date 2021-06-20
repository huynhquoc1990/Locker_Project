import base64
import socket
import struct
import sys
import subprocess
import time
from io import BytesIO
import scapy.all as scapy

from Locker_Project import adafruit_fingerprint


def TaiCauTruc(_Id, _TypeId, _Data, GetData=1):
    if GetData == 1:
        return f'<id>{_Id}</id><type>{_TypeId}</type><data>{_Data}</data>'
    elif GetData == 2:
        return f'<id>{_Id}</id><type>Doorclose</type><data>{_Data}</data>'
    elif GetData == 3:
        return f'<id>{_Id}</id><type>Dooropen</type><data>{_Data}</data>'
    else:
        return f"<id>Error</id><type>{_TypeId}</type><data>{_Data}</data>"
    pass


def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    pass


def shut_down():
    print("shutting down")
    command = "/usr/bin/sudo /sbin/shutdown -h now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print(output)


def UpdateDict(dictupdate, di):
    di.update(dictupdate)
    pass


def Convert1(lst):
    dict1 = {lst[i].split(':')[0]: int(lst[i].split(':')[1]) for i in range(0, len(lst) - 1)}
    return dict1


def sensor_reset(finger):
    """Reset sensor"""
    print("Resetting sensor...")
    if finger.soft_reset() != adafruit_fingerprint.OK:
        print("Unable to reset sensor!")
    print("Sensor is reset.")

def Open_Locker_Test(*args):
    id, typeF, value = [i for i in args[0]]
    host = args[1]
    Port = args[2]
    time.sleep(2)
    dtan = ''
    if int(value) > 16:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM)as Sok:
            Sok.connect((host, Port))
            dtan = bytes(TaiCauTruc(id, 'Dooropen', value, GetData=3), 'utf-8')
            Sok.sendall(len(dtan).to_bytes(4, 'big'))
            Sok.sendall(dtan)
            Sok.close()
    else:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as Sok:
            Sok.connect((host, Port))
            dtan = bytes(TaiCauTruc(id, 'Dooropen', value, GetData=3), 'utf-8')
            Sok.sendall(len(dtan).to_bytes(4, 'big'))
            Sok.sendall(dtan)
            Sok.close()
    pass


def OpenLocker(*args):
    try:
        id, typeF, value = [i for i in args[0]]
        host = args[1]
        Port = args[2]
        lstOutput1 = args[3]
        lstOutput2 = args[4]
        time.sleep(0.5)
        if int(value) > 16:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM)as Sok:
                Sok.connect((host, Port))
                lstOutput2[int(value) - 17].value = False
                dtan = bytes(TaiCauTruc(id, 'Dooropen', value, GetData=3), 'utf-8')
                Sok.sendall(len(dtan).to_bytes(4, 'big'))
                Sok.sendall(dtan)
                Sok.close()
        else:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as Sok:
                Sok.connect((host, Port))
                lstOutput1[int(value) - 1].value = False
                dtan = bytes(TaiCauTruc(id, 'Dooropen', value, GetData=3), 'utf-8')
                Sok.sendall(len(dtan).to_bytes(4, 'big'))
                Sok.sendall(dtan)
                Sok.close()
    except Exception as e:
        print('OpenLocker=:', str(e))
        pass
    pass


def Close_Locker_Test(*args):
    print('Vao Chuong trinh cho dong tu')
    if len(args[0]) == 4:
        id, ty, chek, loker = [i for i in args[0]]  # doi voi truong hop mo bang the tu va Van Tay
        print(args)
    else:
        id, ty, loker = [i for i in args[0]]  # doi voi truong hop mo bang the tu va Van Tay id, ty, loker = [i for i in args[0]]
        print(args)

    host = args[1]
    Port = args[2]

    demtime = time.time()
    time.sleep(1)
    dem = 0
    while time.time() - demtime <= 30:  # chờ tín hiệu dong cua ne: Chờ 3 phut =180s
        dem += 1
        if int(loker) > 16:
            if dem == 10:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as Sok:
                    Sok.connect((host, Port))
                    dtan = bytes(TaiCauTruc(id, 'Doorclose', loker, GetData=2), 'utf-8')
                    Sok.sendall(len(dtan).to_bytes(4, 'big'))
                    Sok.sendall(dtan)
                    Sok.close()
                    break
        else:
            if dem == 11:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as Sok:
                    Sok.connect((host, Port))
                    dtan = bytes(TaiCauTruc(id, 'Doorclose', loker, GetData=2), 'utf-8')
                    Sok.sendall(len(dtan).to_bytes(4, 'big'))
                    Sok.sendall(dtan)
                    Sok.close()
                    break
        time.sleep(1)

def CloseLocker(*args):
    try:
        if len(args[0]) == 4:
            id, ty, chek, loker = [i for i in args[0]]  # doi voi truong hop mo bang the tu va Van Tay
        else:
            id, ty, loker = [i for i in args[0]]

        host = args[1]
        Port = args[2]
        lstOutput1 = args[3]
        lstOutput2 = args[4]
        lstInput1 = args[5]
        lstInput2 = args[6]
        tinhieuchot = args[7]

        demtime = time.time()
        time.sleep(0.5)
        while time.time() - demtime <= 30:  # chờ tín hiệu dong cua ne: Chờ 3 phut =180s
            if int(loker) > 16:
                lstOutput2[int(loker) - 17].value = False
                if lstInput2[int(loker) - 17].value == tinhieuchot:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as Sok:
                        Sok.connect((host, Port))
                        dtan = bytes(TaiCauTruc(id, 'Doorclose', loker, GetData=2), 'utf-8')
                        Sok.sendall(len(dtan).to_bytes(4, 'big'))
                        Sok.sendall(dtan)
                        Sok.close()
                        break
            else:
                lstOutput1[int(loker) - 1].value = False
                if lstInput1[int(loker) - 1].value == tinhieuchot:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as Sok:
                        Sok.connect((host, Port))
                        dtan = bytes(TaiCauTruc(id, 'Doorclose', loker, GetData=2), 'utf-8')
                        Sok.sendall(len(dtan).to_bytes(4, 'big'))
                        Sok.sendall(dtan)
                        Sok.close()
                        break
            time.sleep(1)
    except Exception as e:
        print('CloseLocker :', str(e))
    pass


def Get_my_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


def Scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=0.15, verbose=False)[0]
    clients_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list


def get_default_gateway_linux():
    """Read the default gateway directly from /proc."""
    lst = []
    with open("/proc/net/route") as fh:
        for line in fh:
            fields = line.strip().split()
            if fields[1] != '00000000' or not int(fields[3], 16) & 2:
                # If not default route or not RTF_GATEWAY, skip it
                continue
            lst.append(socket.inet_ntoa(struct.pack("<L", int(fields[2], 16))))
        return lst
        # return socket.inet_ntoa(struct.pack("<L", int(fields[2], 16)))
    pass


def is_connected():
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        socket.create_connection(("1.1.1.1", 53))
        return True
    except OSError:
        print('Khong co ket noi Internet')
        pass
    return False


def restart():
    print("restarting Pi")
    command = "/usr/bin/sudo /sbin/shutdown -r now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print(output)
    pass


def Update():
    if is_connected():
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'Locker-Project'])
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'Locker-Project'])
        restart()
        print('Hoan Thanh')
    else:
        print('Khong ket noi Internet')
        time.sleep(2)
        restart()


def GhiLog():
    pass


text = ''
if __name__ == '__main__':
    Update()
