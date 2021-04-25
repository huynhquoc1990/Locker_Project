import threading
import time
from datetime import datetime
from Locker_Project import Func
tinhieuchot=False
class ScanInput(threading.Thread):
    def __init__(self,lstinput,lstlock,lstID):
        threading.Thread.__init__(self)
        self.lstinput=lstinput
        self.lstlock=lstlock
        self.lstId=lstID
    def run(self):

        while 1:
            now = datetime.now()
            dt_string = now.strftime("%H:%M:%S")
            if dt_string == '23:59:00':
                Func.restart()
            print(dt_string)
            try:
                for i in self.lstId:
                    self.lstlock.acquire()
                    if int(i)>16 and self.lstinput[i]==0:
                        print('Q123')
                        # if lstInput2[int(i)-17].value==tinhieuchot:
                        #     lstOutput2[int(i)-17].value=True
                        #     time.sleep(1)
                        #     lstOutput2[int(i)-17].value=False
                    elif self.lstinput[i]==0:
                        print('Q112')
                        # if lstInput1[int(i)-1].value==tinhieuchot:
                        #     lstOutput1[int(i)-1].value=True
                        #     time.sleep(1)
                        #     lstOutput1[int(i)-1].value=False
                    self.lstlock.release()
                    time.sleep(1)
            except Exception as e:
                print('ScanInput Error: ',str(e))
                # Connect_Device()
                continue