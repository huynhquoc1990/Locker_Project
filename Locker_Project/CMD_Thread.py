import socket
import subprocess
import threading
import time

from Locker_Project import Func

data=''
lstip=[]
class Producer(threading.Thread):
    def __init__(self,Cmd,condition,host,Port,exitEvent,lstthreadStop):
        threading.Thread.__init__(self)
        self.Cmd=Cmd
        self.condition=condition
        self.host=host
        self.Port=Port
        self._Exit=exitEvent
        self.lstThread=lstthreadStop

    @property
    def Exit(self):
        return self._Exit

    @Exit.setter
    def Exit(self,exitEvent):
        self._Exit=exitEvent

    def run(self):
        dem=0
        while 1:
            try:
                if self._Exit.is_set():
                    break
                while 1:
                    if self._Exit.is_set():
                        break
                    full_msg=''
                    data=sock.recv(1024)
                    if len(data)>0:
                        full_msg+=data.decode('utf-8')
                    if len(data)<=1024 and len(data)>0:
                        data = full_msg.split(";")
                        print('check nhan thong tin',data)
                        if data[1]=='Update\n':
                            if Func.is_connected()==True:
                                exit_event = threading.Event()
                                exit_event.set()
                                self._Exit.set()
                                print('Chương trinh dang update....')
                                t1=threading.Thread(target=Func.Update())
                                t1.start()
                                sock.close()
                                # for i in self.lstThread:
                                #     i.start()
                            else:
                                print('Vui Long Kiem Tra Ket Noi internet. Thu Lai...')
                        self.condition.acquire()
                        self.Cmd.append(full_msg)
                        self.condition.notify()
                        self.condition.release()
                        pass
                    full_msg=''
                    if len(data)==0:
                        sock.close()
                        time.sleep(2)
                    time.sleep(0.1)
                    pass
            except Exception as e:
                try:
                    lstip = Func.get_default_gateway_linux()
                    for i in lstip:
                        if i==self.host:
                            break
                        self.host = i
                        try:
                            with socket.socket(socket.AF_INET, socket.SOCK_STREAM)as Sk:
                                Sk.settimeout(5)
                                Sk.connect((self.host, self.Port))
                                Sk.close()
                                print('tim ra host=', self.host)
                        except Exception as e:
                            print(str(e))
                    lstip.clear()

                    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                    sock.settimeout(10)
                    sock.connect_ex((self.host,self.Port))
                    print('Connected')
                except Exception as e:
                    sock.close()
                    pi = subprocess.call(['ping', self.host, '-c1', '-W2', '-q'])
                    print('Ket Qua ping Ip: ',pi)
                    if pi == 0:
                        del pi
                        sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                        dem=0
                        continue
                    else:
                        dem+=1
                        if dem>=5:
                            Func.restart()
            # finally:
            #     if checkwifi()==False:
            #         print('Rasp Pi Zero W turn off wifi. Pls reset Rasp pi')
            #         restart()
    def __del__(self):
        print('Doi tuong preducer bi xoa')