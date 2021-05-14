import base64
import socket
import struct
import sys
import subprocess
import time
from io import BytesIO
import scapy.all as scapy

from Locker_Project import adafruit_fingerprint


def TaiCauTruc(_Id,_TypeId,_Data,GetData=1):
    if GetData==1:
        return f'<id>{_Id}</id><type>{_TypeId}</type><data>{_Data}</data>'
    elif GetData==2:
        return f'<id>{_Id}</id><type>Doorclose</type><data>{_Data}</data>'
    elif GetData==3:
        return f'<id>{_Id}</id><type>Dooropen</type><data>{_Data}</data>'
    else:
        return f"<id>Error</id><type>{_TypeId}</type><data>{_Data}</data>"
    pass

def get_base64_encoded_image(image_path):
    with open(image_path,"rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    pass

def shut_down():
    print ("shutting down")
    command = "/usr/bin/sudo /sbin/shutdown -h now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print (output)

def UpdateDict(dictupdate,di):
    di.update(dictupdate)
    pass

def Convert1(lst):
	dict1={lst[i].split(':')[0]:int(lst[i].split(':')[1]) for i in range(0,len(lst)-1)}
	return dict1

def sensor_reset(finger):
    """Reset sensor"""
    print("Resetting sensor...")
    if finger.soft_reset() != adafruit_fingerprint.OK:
        print("Unable to reset sensor!")
    print("Sensor is reset.")
'''Lấy ảnh image từ finger, mặc định được lấy về ảnh có định dạng jpg'''
# def Get_Finger_Image(finger,signak=True):
#     """Scan fingerprint then save image to filename."""
#     times=time.time()
#     check=False
#     try:
#         while ((time.time()-times<=30) and signak==True):
#             i = finger.get_image()
#             if i == adafruit_fingerprint.OK:
#                 check=True
#                 break
#             if i == adafruit_fingerprint.NOFINGER:
#                 print(".", end="", flush=True)
#                 #blynk.notify('Read Finger: Khong Phai Dau Van Tay')
#             elif i == adafruit_fingerprint.IMAGEFAIL:
#                 #blynk.notify('Imaging error')
#                 print("Read Finger: Imaging error")
#                 return False
#             else:
#                 print("Other error")
#                 #blynk.notify('Read Finger: Other error')
#                 return False
#         if check==False:
#             return False
#
#         # let PIL take care of the image headers and file structure
#         from PIL import Image  # pylint: disable=import-outside-toplevel
#         img= Image.new("L", (256, 288), "white")#256, 288
#         pixeldata = img.load()
#         mask = 0b00001111
#         result = finger.get_fpdata(sensorbuffer="image")
#         x = 0
#         y = 0
#         for i in range(len(result)):
#             pixeldata[x, y] = (int(result[i]) >> 4) * 17
#             x += 1
#             pixeldata[x, y] = (int(result[i]) & mask) * 17
#             if x == 255:
#                 x = 0
#                 y += 1
#             else:
#                 x += 1
#         buffer = BytesIO()
#         img.save(buffer,format="PNG") #Enregistre l'image dans le buffer
#         myimage = buffer.getvalue()
#         return base64.b64encode(myimage).decode('utf-8')
#     except Exception as e:
#         print('Loi Doc Van Tay',str(e))
#         #blynk.notify('Loi Doc Van Tay',str(e))
#         return False

def OpenLocker(*args):
    try:
        id,typeF,value=[i for i in args[0]]
        host=args[1]
        Port=args[2]
        lstOutput1=args[3]
        lstOutput2=args[4]
        demtime=time.time()
        time.sleep(2)
        if int(value)>16:
            with socket.socket(socket.AF_INET,socket.SOCK_STREAM)as Sok:
                Sok.connect((host,Port))
                lstOutput2[int(value)-17].value=False
                dtan=bytes(TaiCauTruc(id,'Dooropen',value.split("\n")[0],GetData=3),'utf-8')
                Sok.sendall(len(dtan).to_bytes(4,'big'))
                Sok.sendall(dtan)
                Sok.close()
        else:
            with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as Sok:
                Sok.connect((host,Port))
                lstOutput1[int(value)-1].value=False
                dtan=bytes(TaiCauTruc(id,'Dooropen',value.split("\n")[0],GetData=3),'utf-8')
                Sok.sendall(len(dtan).to_bytes(4,'big'))
                Sok.sendall(dtan)
                Sok.close()
    except Exception as e:
        print('OpenLocker=:',str(e))
        pass
    pass

def CloseLocker(*args):
    try:
        id,ty,loker=[i for i in args[0]]
        host = args[1]
        Port = args[2]
        lstOutput1 = args[3]
        lstOutput2 = args[4]
        lstInput1=args[5]
        lstInput2=args[6]
        tinhieuchot=args[7]

        demtime=time.time()
        time.sleep(2)
        while time.time()-demtime<=30:# chờ tín hiệu dong cua ne: Chờ 3 phut =180s
            if int(loker)>16:
                lstOutput2[int(loker)-17].value=False
                if lstInput2[int(loker)-17].value==tinhieuchot:

                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as Sok:
                        Sok.connect((host, Port))
                        dtan=bytes(TaiCauTruc(id,'Doorclose',loker.split("\n")[0],GetData=2),'utf-8')
                        Sok.sendall(len(dtan).to_bytes(4,'big'))
                        Sok.sendall(dtan)
                        Sok.close()
                        break
            else:
                lstOutput1[int(loker)-1].value=False
                if lstInput1[int(loker)-1].value==tinhieuchot:

                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as Sok:
                        Sok.connect((host, Port))
                        dtan=bytes(TaiCauTruc(id,'Doorclose',loker.split("\n")[0],GetData=2),'utf-8')
                        Sok.sendall(len(dtan).to_bytes(4,'big'))
                        Sok.sendall(dtan)
                        Sok.close()
                        break
            time.sleep(1)
    except Exception as e:
        print('CloseLocker :',str(e))
    pass

def save_fingerprint_image(dta,host,Port,finger):
    """Scan fingerprint then save image to filename."""
    msg=Get_Finger_Image(finger=finger,signak=True)
    if msg==False:
        print('Khong co van Tay')
        return False
    dta1=TaiCauTruc(dta[0],dta[1].split('\n')[0],msg)
    dta2=bytes(dta1,'utf-8')
    size=len(dta2)
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sock:
        sock.connect((host,Port))
        sock.sendall(size.to_bytes(4,byteorder='big'))
        sock.sendall(dta2)
        sock.close()
        del msg,dta1
        return  True
    return False


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
    lst=[]
    with open("/proc/net/route") as fh:
        for line in fh:
            fields = line.strip().split()
            if fields[1] != '00000000' or not int(fields[3], 16) & 2:
                # If not default route or not RTF_GATEWAY, skip it
                continue
            lst.append(socket.inet_ntoa(struct.pack("<L", int(fields[2], 16))))
        return lst
            #return socket.inet_ntoa(struct.pack("<L", int(fields[2], 16)))
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
    print ("restarting Pi")
    command = "/usr/bin/sudo /sbin/shutdown -r now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print (output)
    pass
def Update():
    if is_connected()==True:
        subprocess.check_call([sys.executable, '-m','pip', 'install','--upgrade','Locker-Project'])
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'Locker-Project'])
        restart()
        print('Hoan Thanh')
    else:
        print('Khong ket noi Internet')
        time.sleep(2)
        restart()

def GhiLog():

    pass

text='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'

if __name__ == '__main__':
    Update()