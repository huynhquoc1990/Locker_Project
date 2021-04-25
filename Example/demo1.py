import socket
import threading
import time

import serial

import Locker_Project.Locker
from Locker_Project import CMD_ScanInput, CMD_Thread, CMD_Process, Func,Locker

host='192.168.100.9'
Port=3003
threamain=[]
lstID=[]
lstLocker={}
lst=['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30']

lstInput1=[]
lstInput2=[]
lstOutput1=[]
lstOutput2=[]


#uart = serial.Serial("/dev/ttyS0", baudrate=528000, timeout=1)#489600  528000
#finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

Danhsachtu=[] # chứa và quản lý danh sách tủ

def Update():
    import sys
    import subprocess
    # Go Chuong trinh
    subprocess.check_call([sys.executable, '-m', 'pip', 'uninstall', 'Locker-Project'])
    print('Hoan Thanh Go chuong Trinh')
    # implement pip as a subprocess:
    print(subprocess.check_call([sys.executable, 'sudo','pip', 'install','Locker-Project']))
    print('Hoan Thanh')


def main():
    try:
        chuoi = '<id>1212</id><type>getdata</type><data>statusdoor</data>'
        chuoi = chuoi.encode('utf-8')
        size = len(chuoi)
        while 1:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as scok112:
                    scok112.connect((host, Port))
                    scok112.sendall(size.to_bytes(4, byteorder='big'))
                    scok112.sendall(chuoi)
                    msg = scok112.recv(1024)
                    dta = msg.decode('utf-8')
                    id = dta.split(';')[0]
                    ref = dta.split(';')[1].split('\n')[0].split('/')
                    print(ref)
                    if id == '1212':
                        lstLocker = Func.Convert1(ref)
                        print(lstLocker)
                    scok112.close()
                    break
            except Exception as e:
                scok112.close()
                print('Loi Roi')
        time.sleep(2)

        condition=threading.Condition()
        lstLock=threading.Lock()

        producer=CMD_Thread.Producer(Cmd=lstID,condition=condition,host=host,Port=Port)
        threamain.append(producer)

        fingerT=CMD_Process.CMD_Process(lstID,condition,lstLocker,lstLock)
        threamain.append(fingerT)
        scan = CMD_ScanInput.ScanInput(lstinput=lstLocker, lstlock=lstLock,lstID=lst)
        threamain.append(scan)
        for t in threamain:
            t.start()

    except Exception as e:
        print('Connect Mysql Error:',str(e))

if __name__ == '__main__':
    Update()