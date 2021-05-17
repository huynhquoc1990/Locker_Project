import socket
import threading
import time
from Locker_Project import Func

class MyTask_Tag(threading.Thread):
    status=False
    def __init__(self,mes,lstInput,lstLock,TypeReader,host,Port,input1,input2,output1,output2,tinhieuchot,Pn532,demvantay,main):
        threading.Thread.__init__(self)
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
        self._Reader=Pn532
        self.demvantay=demvantay
        self.processMain=main
    @property
    def Reader(self):
        return self._Reader
    @Reader.setter
    def Reader(self,pn532):
        self._Reader=pn532

    @property
    def Exit(self):
        return self.signal
    @Exit.setter
    def Exit(self,signal):
        self.signal=signal
    @property
    def Dem(self):
        return self.demvantay
    @Dem.setter
    def Dem(self,dem):
        self.demvantay=dem

    def run(self):
        valueTag = ''
        if len(self.mes)==2:
            id,value1= [i for i in self.mes]
            lmg=0

            times=time.time()
            if self.TypeRead=='Copen':
                try:
                    while (self.signal==True):
                        if time.time()-times>=30:
                            self.processMain.Thetudangdoc==False
                            self.Exit=False
                        if self.processMain.Thetudangdoc==False:
                            self.processMain.Thetudangdoc==True
                            uid = self._Reader.read_passive_target(timeout=0.5)
                            if uid is not None:
                                valueTag=''.join([hex(i) for i in uid])
                                print(valueTag)
                                self.processMain.Thetudangdoc==False
                                self.processMain.STATUS=True
                                self.Exit=False
                                lmg=2
                            self._Reader.power_down()
                            self.processMain.Thetudangdoc==False

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
                            self.processMain.ClearThread()

                        except Exception as e:
                            sock.close()
                            self.processMain.ClearThread()
                            self.processMain.Thetudangdoc==False
                            self.processMain.STATUS=True
                            print("MyTask_Tag:", str(e))
                            # self._blynk.notify('MyTask_Tag: ' + str(e))
                except Exception as e:
                    print("MyTask_Tag:", str(e))
                    self.processMain.ClearThread()
                    self.processMain.Thetudangdoc==False
                    self.processMain.STATUS=True

                    #self._blynk.notify('MyTask_Tag: ' + str(e))
        if len(self.mes)==3:
            id,typevalue,value= [i for i in self.mes]
            lmg=0
            times=time.time()
            if self.TypeRead=='Cused':
                try:
                    while (self.signal==True):
                        if time.time()-times>=30:
                            self.processMain.ClearThread()
                            self.processMain.STATUS=True
                            self.Exit=False
                        if self.processMain.Thetudangdoc==False:

                            self.processMain.Thetudangdoc=True
                            uid = self._Reader.read_passive_target(timeout=0.5)
                            if uid is not None:
                                valueTag=''.join([hex(i) for i in uid])
                                print(valueTag)
                                self.processMain.ClearThread()
                                self.Exit=False
                                lmg=2
                            self._Reader.power_down()
                            self.processMain.Thetudangdoc=False
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
                                sock11.close()
                            self.processMain.ClearThread()
                        except Exception as e:
                            sock11.close()
                            self.processMain.ClearThread()
                            self.processMain.Thetudangdoc==False
                            print("MyTask_Tag1:",str(e))
                            #self._blynk.notify("MyTask_Tag1: "+str(e))
                except Exception as e:
                    print("MyTask_Tag2:",str(e))
                    self.processMain.ClearThread()
                    self.processMain.Thetudangdoc==False

                    #self._blynk.notify("MyTask_Tag2: " + str(e))
    def __del__(self):
        print(self.name,' Đã bị xóa')