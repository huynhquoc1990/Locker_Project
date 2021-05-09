import threading
import time
from datetime import datetime
from Locker_Project import Func
tinhieuchot=False
class ScanInput(threading.Thread):
    def __init__(self,lstinput,lstlock,lstID,exitEvent,input1,input2,output1,output2,blynk):
        threading.Thread.__init__(self)
        self.lstinput=lstinput
        self.lstlock=lstlock
        self.lstId=lstID
        self._Exit=exitEvent
        self._Input1=input1
        self._Input2=input2
        self._Output1=output1
        self._Output2=output2
        self.host=''
        self._blynk=blynk
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
        while 1:
            now = datetime.now()
            dt_string = now.strftime("%H:%M:%S")
            if dt_string == '23:59:00':
                #self._blynk.notify('Thread Scan Restart Raspi With 24:00:00')
                Func.restart()
            print(dt_string)
            if self._Exit.is_set():
                #self._blynk.notify('Thread Scan input Stop')
                break
            try:
                for i in self.lstId:
                    if self._Exit.is_set():
                        #self._blynk.notify('Thread Scan input Stop')
                        break
                    self.lstlock.acquire()
                    if int(i)>16 and self.lstinput[i]==0:
                        print('Tu So',i)
                        if self._Input2[int(i)-17].value==tinhieuchot:
                            self._Output2[int(i)-17].value=True
                            time.sleep(1)
                            self._Output2[int(i)-17].value=False
                    elif self.lstinput[i]==0:
                        print('Tu So',i)
                        if self._Input1[int(i)-1].value==tinhieuchot:
                            self._Output1[int(i)-1].value=True
                            time.sleep(1)
                            self._Output1[int(i)-1].value=False
                    self.lstlock.release()

                    time.sleep(1)

            except Exception as e:
                print('ScanInput Error: ',str(e))
                #self._blynk.notify('ScanInput Error: '+str(e))
                continue