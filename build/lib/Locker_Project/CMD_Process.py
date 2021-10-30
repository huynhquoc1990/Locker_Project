import threading
import time
import socket
from Locker_Project import Func, MyTask_Finger, MyTask_Tag
from Locker_Project.Func import TaiCauTruc


class Class_Thread:
    def __init__(self, name, ObjectThread):
        self.Name = name
        self.Object = ObjectThread

    @property
    def ThreadName(self):
        return self.Name

    @ThreadName.setter
    def ThreadName(self, name):
        self.Name = name

    @property
    def Thread_Object(self):
        return self.Object

    @Thread_Object.setter
    def Thread_Object(self, thread):
        self.Object = thread
        pass


class Cmd_Process(threading.Thread):
    exit_event = threading.Event()

    condition = threading.Thread()

    def __init__(self, finger, pn532, Cmd, condition, lst_input, lstLock, exitEvent, input1, input2, output1, output2,
                 host, Port, uart, tinhieuchot):
        threading.Thread.__init__(self)
        self.finger = finger
        self.pn532 = pn532
        self.Cmd = Cmd
        self.condition = condition
        self.ListThread = []
        self.lstinput = lst_input
        self.lstLock = lstLock
        self._Exit = exitEvent
        self._input1 = input1
        self._input2 = input2
        self._output1 = output1
        self._output2 = output2
        self.host = host
        self.Port = Port
        self.uart = uart
        self.tinhieuchot = tinhieuchot

    @property
    def Exit(self):
        return self._Exit

    @Exit.setter
    def Exit(self, exitEvent):
        self._Exit = exitEvent

    @property
    def Host(self):
        return self.host

    @Host.setter
    def Host(self, host):
        self.host = host

    ThreadFinger = Class_Thread(None, None)  # dungf ddeer gan thread
    ThreadTag = Class_Thread(None, None)
    KiemsoatSoLanDocSaiThe = 0

    def doConnect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((self.host, self.Port))
            ThreadMain = '<id>121</id><type>socket</type><data>send</data>'  # <type>socket</type><data>send</data>
            ThreadMain = ThreadMain.encode('utf-8')
            size = len(ThreadMain)
            sock.sendall(size.to_bytes(4, byteorder='big'))
            sock.sendall(ThreadMain)
        except socket.error:
            sock.close()
            pass
        return sock

    def run(self):

        sock_send = self.doConnect()

        t1 = MyTask_Finger.MyTask_Finger(
            finger=self.finger,
            namefileImg="fingerprint.jpg",
            lstInput=self.lstinput,
            lstLock=self.lstLock,
            input1=self._input1,
            input2=self._input2,
            output1=self._output1,
            output2=self._output2,
            host=self.host,
            Port=self.Port,
            uart=self.uart,
            main=self
        )

        t2 = MyTask_Tag.MyTask_Tag(
            lstInput=self.lstinput,
            lstLock=self.lstLock,
            host=self.host,
            Port=self.Port,
            input1=self._input1,
            input2=self._input2,
            output1=self._output1,
            output2=self._output2,
            Pn532=self.pn532,
            main=self
        )
        while 1:
            if self._Exit.is_set():
                break
            self.condition.acquire()
            while 1:
                if len(self.Cmd) > 0:
                    dta = self.Cmd.pop().split(";")
                    if (dta[1] == 'Fused' or dta[1] == 'Cused') and dta[2] == "OK":
                        self.lstLock.acquire()
                        sic1 = {dta[3]: 1}
                        Func.UpdateDict(sic1, self.lstinput)
                        self.lstLock.release()
                        try:
                            if int(dta[3]) > 16:
                                self._output2[int(dta[3]) - 17].value = True
                            else:
                                self._output1[int(dta[3]) - 1].value = True

                            t10 = threading.Thread(
                                target=Func.CloseLocker,
                                args=[dta, self.host, self.Port, self._output1, self._output2, self._input1,
                                      self._input2, self.tinhieuchot]
                            )
                            t10.start()
                        except Exception as Loi3:
                            print('Loi Chua co Board Io', str(Loi3))
                        break
                    if (dta[1] == 'Fused' and dta[2] != "OK") or dta[1] == 'Fopen' or dta[1] == 'FDK':
                        if self.ThreadFinger.ThreadName is None:
                            self.ThreadFinger.ThreadName = 'th'
                            self.ThreadFinger.Thread_Object = t1
                            break

                        elif self.ThreadFinger.Name != 'finger_print':
                            if self.ThreadTag.ThreadName is not None:
                                self.ThreadTag.Thread_Object.raise_exception()
                            self.ThreadFinger.Thread_Object.raise_exception()

                            t11 = MyTask_Finger.MyTask_Finger(
                                finger=self.finger, namefileImg="fingerprint.jpg",
                                lstInput=self.lstinput, lstLock=self.lstLock,
                                input1=self._input1, input2=self._input2,
                                output1=self._output1, output2=self._output2,
                                host=self.host, Port=self.Port,
                                uart=self.uart, main=self
                            )
                            self.ThreadFinger.ThreadName = 'finger_print'
                            self.ThreadFinger.Thread_Object = t11
                            self.ThreadFinger.Thread_Object.mes = dta
                            self.ThreadFinger.Thread_Object.TypeRead = dta[1]
                            self.ThreadFinger.Thread_Object.start()
                            break
                        elif self.ThreadFinger.Thread_Object.is_alive():
                            self.ThreadFinger.Thread_Object.mes = dta
                            self.ThreadFinger.Thread_Object.TypeRead = dta[1]
                    if (dta[1] == 'Cused' and dta[2] != "OK") or dta[1] == 'Copen':
                        if self.ThreadTag.ThreadName is None:
                            self.ThreadTag.ThreadName = 'te'
                            self.ThreadTag.Thread_Object = t2
                            break

                        elif self.ThreadTag.ThreadName != 'Cused':

                            if self.ThreadFinger.ThreadName is not None:
                                self.ThreadFinger.Thread_Object.raise_exception()

                            self.ThreadTag.Thread_Object.raise_exception()
                            t21 = MyTask_Tag.MyTask_Tag(
                                lstInput=self.lstinput, lstLock=self.lstLock,
                                host=self.host, Port=self.Port,
                                input1=self._input1, input2=self._input2,
                                output1=self._output1, output2=self._output2,
                                Pn532=self.pn532, main=self
                            )

                            self.ThreadTag.ThreadName = 'Cused'
                            self.ThreadTag.Thread_Object = t21
                            self.ThreadTag.Thread_Object.mes = dta
                            self.ThreadTag.Thread_Object.TypeRead = dta[1]
                            self.ThreadTag.Thread_Object.start()
                            break
                        elif self.ThreadTag.Thread_Object.is_alive():
                            self.ThreadTag.Thread_Object.mes = dta
                            self.ThreadTag.Thread_Object.TypeRead = dta[1]

                    if dta[1] == 'Cancel':
                        self.lstLock.acquire()
                        sic1 = {dta[2]: 0}
                        Func.UpdateDict(sic1, self.lstinput)
                        self.lstLock.release()
                        break
                    if dta[1] == 'Pused':
                        self.lstLock.acquire()
                        sic1 = {dta[2]: 1}
                        Func.UpdateDict(sic1, self.lstinput)
                        self.lstLock.release()
                        try:
                            if int(dta[2]) > 16:
                                self._output2[int(dta[2]) - 17].value = True
                            else:
                                self._output1[int(dta[2]) - 1].value = True

                            t5 = threading.Thread(
                                target=Func.CloseLocker,
                                args=[dta, self.host, self.Port, self._output1, self._output2, self._input1,
                                      self._input2, self.tinhieuchot]
                            )
                            t5.start()
                        except Exception as Loi2:
                            print('Loi Chua co Board Io', str(Loi2))
                        break

                    if dta[1] == "Dooropen":
                        self.lstLock.acquire()
                        sic1 = {dta[2]: 0}
                        Func.UpdateDict(sic1, self.lstinput)
                        self.lstLock.release()
                        try:
                            if int(dta[2]) > 16:
                                self._output2[int(dta[2]) - 17].value = True
                                time.sleep(0.3)
                                self._output2[int(dta[2]) - 17].value = False
                            else:
                                self._output1[int(dta[2]) - 1].value = True
                                time.sleep(0.3)
                                self._output1[int(dta[2]) - 1].value = False

                            Chuoi = bytes(TaiCauTruc(dta[0], 'Dooropen', dta[2], GetData=3), 'utf-8')
                            print(Chuoi)
                            sock_send.sendall(len(Chuoi).to_bytes(4, 'big'))
                            sock_send.sendall(Chuoi)
                        except socket.error:
                            time.sleep(3)
                            sock_send = self.doConnect()
                        except Exception as Loi1:
                            print('Loi Chua co Board Io', str(Loi1))
                            sock_send = self.doConnect()
                        break
                break
            self.condition.wait()
            self.condition.release()
