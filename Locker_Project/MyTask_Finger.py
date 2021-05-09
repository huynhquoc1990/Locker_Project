import socket
import threading
import time

from Locker_Project import Func
class MyTask_Finger(threading.Thread):
    def __init__(self,finger,mes,namefileImg,lstInput,lstLock,TypeReader,host,Port,input1,input2,output1,output2,tinhieuchot):
        threading.Thread.__init__(self)
        self.finger=finger
        self.signal=True
        self.namefileImg=namefileImg
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
        if len(self.mes)==2:
            id,value1= [i for i in self.mes]
            times=time.time()
            if self.TypeRead=='Fopen':
                valueFinger=Func.Get_Finger_Image(finger=self.finger,signak=self.signal)
                if valueFinger==False:
                    return False
                try:
                    dta1=bytes(Func.TaiCauTruc(id,'Fopen',valueFinger),'utf-8')
                    size=len(dta1)
                    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sock:
                        sock.connect((self.host,self.Port))
                        sock.sendall(size.to_bytes(4,byteorder='big'))
                        sock.sendall(dta1)
                        del dta1
                        sock.close()
                except Exception as e:
                    print("MyTask_Finger:",str(e))
                    #self._blynk.notify('Fused MyTask_Finger: ' + str(e))
                    Func.sensor_reset(self.finger)
        if len(self.mes)==3:
            id,typevalue,value= [i for i in self.mes]
            times=time.time()
            if self.TypeRead=='Fused':
                valueFinger=Func.Get_Finger_Image(finger=self.finger,signak=self.signal)
                if valueFinger==False:
                    return False
                try:
                    dta1=bytes(Func.TaiCauTruc(id,typevalue,valueFinger),'utf-8')
                    size=len(dta1)
                    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sock1:
                        sock1.connect((self.host,self.Port))
                        sock1.sendall(size.to_bytes(4,byteorder='big'))
                        sock1.sendall(dta1)
                        del dta1
                        buff=sock1.recv(1024)
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
                            print('Van Tay Chưa Đúng')
                            #self._blynk.notify('Fused MyTask_Finger: ' + 'Van Tay Chưa Đúng')
                            sock1.close()
                except Exception as e:
                    print("MyTask_Finger:",str(e))
                    #self._blynk.notify("MyTask_Finger: "+str(e))
    def __del__(self):
        print(self.name,'thread myTag_Finger bi Xoa')
        #self._blynk.notify(self.name+'thread myTag_Finger bi Xoa')
