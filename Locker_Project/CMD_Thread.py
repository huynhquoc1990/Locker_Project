import socket
import subprocess
import threading
import time

from Locker_Project import Func

data=''
lstip=[]

class Producer(threading.Thread):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
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


    @property
    def Host(self):
        return self.host
    @Host.setter
    def Host(self,host):
        self.host=host

    def run(self):
        check=False
        self.sock.connect((self.Host,self.Port))
        while 1:
            time.sleep(0.5)
            try:
                if self._Exit.is_set():
                    break
                while 1:
                    if self._Exit.is_set():
                        break
                    full_msg=''
                    data=self.sock.recv(1024)
                    if len(data)>0:
                        full_msg+=data.decode('utf-8')
                    if len(data)<=1024 and len(data)>0:
                        data = full_msg.split(";")
                        print('check nhan thong tin',data)
                        #self._blynk.notify('check nhan thong tin ' +str(data))
                        if data[1]=='Update\n':
                            if Func.is_connected()==True:
                                exit_event = threading.Event()
                                exit_event.set()
                                self._Exit.set()
                                print('Chương trinh dang update....')
                                #self._blynk.notify('Chương trinh dang update....')
                                t1=threading.Thread(target=Func.Update())
                                t1.start()
                                self.sock.close()
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
                        self.sock.close()
                        check=True
                    time.sleep(0.1)
                    pass
            except Exception as e:
                print(str(e))
                try:
                    lstip = Func.get_default_gateway_linux()
                    for i in lstip:
                        if i==self.Host:
                            break
                        self.Host = i
                        check=True
                        try:
                            with socket.socket(socket.AF_INET, socket.SOCK_STREAM)as Sk:
                                Sk.settimeout(5)
                                Sk.connect((self.Host, self.Port))
                                Sk.close()
                                print('tim ra host=', self.Host)
                                #self._blynk.notify('Chương trinh dang update....')
                                for t in self.lstThread:
                                    t.Host = self.Host
                        except Exception as e:
                            print(str(e))
                            #self._blynk.notify(str(e))
                    lstip.clear()
                    if check==True:
                        self.sock.close()
                        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                        self.sock.settimeout(10)
                        try:
                            self.sock.connect((self.Host,self.Port))
                            check=False
                            print('Connected')
                            #self._blynk.notify('Connected')
                        except Exception as e:
                            print('Mat ket noi',str(e))
                            #self._blynk.notify('Mat ket noi: '+str(e))
                except Exception as e:
                    print(str(e))
                    #self._blynk.notify(str(e))
                    self.sock.close()
                    continue
    def __del__(self):
        print('Doi tuong preducer bi xoa')