import socket
import threading
import time
from io import BytesIO
from Locker_Project import adafruit_fingerprint
from Locker_Project import Func
import base64

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
    @property
    def Exit(self):
        return self.signal
    @Exit.setter
    def Exit(self,signal):
        self.signal=signal

    def Get_Finger_Image(self):
        """Scan fingerprint then save image to filename."""
        times=time.time()
        check=False
        try:
            while ((time.time()-times<=30) and self.signal==True):
                i = self.finger.get_image()
                if i == adafruit_fingerprint.OK:
                    check=True
                    break
                if i == adafruit_fingerprint.NOFINGER:
                    print(".", end="", flush=True)
                    #blynk.notify('Read Finger: Khong Phai Dau Van Tay')
                # elif i == adafruit_fingerprint.IMAGEFAIL:
                #     #blynk.notify('Imaging error')
                #     print("Read Finger: Imaging error")
                #     return False
                # else:
                #     print("Other error")
                #     #blynk.notify('Read Finger: Other error')
                #     return False
            if check==False:
                return False

            # let PIL take care of the image headers and file structure
            from PIL import Image  # pylint: disable=import-outside-toplevel
            img= Image.new("L", (256, 288), "white")#256, 288
            pixeldata = img.load()
            mask = 0b00001111
            result = self.finger.get_fpdata(sensorbuffer="image")
            x = 0
            y = 0
            for i in range(len(result)):
                pixeldata[x, y] = (int(result[i]) >> 4) * 17
                x += 1
                pixeldata[x, y] = (int(result[i]) & mask) * 17
                if x == 255:
                    x = 0
                    y += 1
                else:
                    x += 1
            buffer = BytesIO()
            img.save(buffer,format="PNG") #Enregistre l'image dans le buffer
            myimage = buffer.getvalue()
            return base64.b64encode(myimage).decode('utf-8')
        except Exception as e:
            print('Loi Doc Van Tay',str(e))
            #blynk.notify('Loi Doc Van Tay',str(e))
            return False
    def run(self):
        if len(self.mes)==2:
            id,value1= [i for i in self.mes]
            times=time.time()
            if self.TypeRead=='FDK':
                msg=self.Get_Finger_Image()
                if msg==False:
                    print('Khong co van Tay')
                    return False
                dta1=Func.TaiCauTruc(id,value1.split('\n')[0],msg)
                dta2=bytes(dta1,'utf-8')
                size=len(dta2)
                with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sck:
                    sck.connect((self.host,self.Port))
                    sck.sendall(size.to_bytes(4,byteorder='big'))
                    sck.sendall(dta2)
                    sck.close()
                    del msg,dta1
                    return  True
                return False
                pass

            if self.TypeRead=='Fopen':
                valueFinger=self.Get_Finger_Image()
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
                valueFinger=self.Get_Finger_Image()

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
