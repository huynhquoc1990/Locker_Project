import socket
import threading
import time
from Locker_Project import Func

class MyTask_Tag(threading.Thread):
    def __init__(self,pn532,mes,lstInput,lstLock,TypeReader,host,Port,input1,input2,output1,output2,tinhieuchot):
        threading.Thread.__init__(self)
        self.pn532=pn532
        self.signal=True
        self.mes=mes
        self.lstInput=lstInput
        self.listLock=lstLock
        self.TypeRead=TypeReader
        self.host=host
        self.Port=Port
        self._input1=input1
        self._input2=input2
        self._output1=output1
        self._output2=output2
        self._tinhieuchot=tinhieuchot

    def run(self):
        valueTag = ''
        if len(self.mes)==2:
            id,value1= [i for i in self.mes]
            lmg=0

            times=time.time()
            if self.TypeRead=='Copen':
                try:
                    while (self.signal==True ):
                        if time.time()-times>=3:
                            self.signal=False
                        uid = self.pn532.read_passive_target(timeout=0.5)
                        if uid is not None:
                            valueTag=''.join([hex(i) for i in uid])
                            self.signal=False
                            lmg=2
                        self.pn532.power_down()

                    if lmg==2 and valueTag!='':
                        try:
                            dta1=bytes(Func.TaiCauTruc(id,'Copen',valueTag),'utf-8')
                            size=len(dta1)
                            with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sock:
                                sock.connect((self.host,self.Port))
                                sock.sendall(size.to_bytes(4,byteorder='big'))
                                sock.sendall(dta1)
                                sock.close()
                                del dta1
                        except Exception as e:
                            print("MyTask_Tag:", str(e))
                            # self._blynk.notify('MyTask_Tag: ' + str(e))
                except Exception as e:
                    print("MyTask_Tag:", str(e))
                    #self._blynk.notify('MyTask_Tag: ' + str(e))
        if len(self.mes)==3:
            id,typevalue,value= [i for i in self.mes]
            lmg=0
            times=time.time()
            if self.TypeRead=='Cused':
                try:
                    while (self.signal==True ):
                        if time.time()-times>=3:
                            self.signal=False
                        uid = self.pn532.read_passive_target(timeout=0.5)
                        if uid is not None:
                            valueTag=''.join([hex(i) for i in uid])
                            self.signal=False
                            lmg=2
                        self.pn532.power_down()
                        pass

                    if lmg==2 and valueTag!='':
                        try:
                            dta1=bytes(Func.TaiCauTruc(id,typevalue,valueTag),'utf-8')
                            size=len(dta1)
                            with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sock11:
                                sock11.connect((self.host,self.Port))
                                sock11.sendall(size.to_bytes(4,byteorder='big'))
                                sock11.sendall(dta1)
                                del dta1
                                buff=sock11.recv(1024)
                                dk1=buff.decode('utf-8').split(";")[2]
                                if dk1=='OK\n':
                                    self.listLock.acquire()
                                    id=value.split('\n')[0]
                                    sic1={id:1}
                                    Func.UpdateDict(sic1,self.lstInput)
                                    self.listLock.release()
                                    #self._blynk.notify("Tu {} duoc kich hoat".format(id))
                                    if int(value)>16:
                                        self._output2[int(value)-17].value=True
                                    else:
                                        self._output1[int(value)-1].value=True
                                    t1=threading.Thread(target=Func.CloseLocker,args=[self.mes,self.host,self.Port,self._output1,self._output2,self._input1,self._input2,self._tinhieuchot])
                                    t1.start()
                                else:
                                    print('Kiem tra lai the')
                                    #self._blynk.notify('Kiem tra lai the')
                                    sock11.close()
                        except Exception as e:
                            print("MyTask_Tag1:",str(e))
                            #self._blynk.notify("MyTask_Tag1: "+str(e))
                except Exception as e:
                    print("MyTask_Tag2:",str(e))
                    #self._blynk.notify("MyTask_Tag2: " + str(e))
    def __del__(self):
        print(self.name,' Đã bị xóa')