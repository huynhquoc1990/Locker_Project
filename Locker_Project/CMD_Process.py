import threading
import time
from Locker_Project import Func, MyTask_Finger, MyTask_Tag


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


class Class_Thread_Tag:
    def __init__(self,name,Obthread):
        self.Name=name
        self.Object=Obthread


class CMD_Process(threading.Thread):
    exit_event = threading.Event()
    STATUS = True
    TrangThaiTheTu = True

    vantaydangdoc = False
    Thetudangdoc = False
    lstThread = []


    whileVantay = False
    whileThetu = True
    condition = threading.Thread()

    def __init__(self, finger, pn532, Cmd, condition, lst_input, lstLock, exitEvent, input1, input2, output1, output2, host, Port, uart, tinhieuchot ):
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

    def ClearThread(self):
        self.lstThread.clear()
        self.STATUS = True


    def run(self):
        while 1:
            if self._Exit.is_set():
                break
            self.condition.acquire()
            while 1:
                print(self.Cmd)
                if len(self.Cmd) > 0:
                    dta = self.Cmd.pop().split(";")
                    print('Tramg thai Cảm Biến vân Tay', self.STATUS)
                    print('Tramg thai Thẻ Từ', self.TrangThaiTheTu)
                    # try:
                    if (dta[1] == 'Fused' or dta[1] == 'Cused') and dta[2] == "OK":
                        self.lstLock.acquire()
                        id = dta[3].split('\n')[0]
                        print('id=', id)
                        sic1 = {id: 1}
                        Func.UpdateDict(sic1, self.lstinput)
                        self.lstLock.release()
                        # self._blynk.notify("Tu {} duoc kich hoat".format(id))
                        try:
                            if int(dta[3]) > 16:
                                self._output2[int(dta[3]) - 17].value = True
                            else:
                                self._output1[int(dta[3]) - 1].value = True
                            t10 = threading.Thread(target=Func.CloseLocker,
                                                   args=[dta, self.host, self.Port, self._output1, self._output2,
                                                         self._input1, self._input2, self.tinhieuchot])
                            t10.start()
                        except Exception as Loi3:
                            print('Loi Chua co Board Io',str(Loi3))
                        break

                    if dta[1] == 'Fused' and dta[2] != "OK\n":
                        self.whileVantay = True
                        self.whileThetu = False

                        for i in self.lstThread:
                            # if i.Name != 'dk':
                                # if not self.vantaydangdoc: #
                            i.Object.signal = False
                        self.ClearThread()
                        time.sleep(1)
                        # if self.STATUS:
                        #     self.STATUS = False
                        if len(self.lstThread) == 0:
                            t1 = MyTask_Finger.MyTask_Finger(finger=self.finger, mes=dta, namefileImg="fingerprint.jpg",
                                                                 lstInput=self.lstinput, lstLock=self.lstLock, TypeReader=dta[1].split("\n")[0], input1=self._input1,
                                                                 input2=self._input2, output1=self._output1, output2=self._output2, host=self.host,
                                                                 Port=self.Port, uart=self.uart, main=self)
                            threadOPen = Class_Thread('dk', t1)
                            self.lstThread.append(threadOPen)
                            t1.start()
                            break
                    if (dta[1] == 'Cused') and dta[2] != "OK\n":
                        # for i in self.lstThread:
                        #     if i.Set_GetName != 'CTag':
                        #         if self.Thetudangdoc == False: #
                        #             i.Thread_.Exit = False
                        #         self.ClearThread()
                        #     pass
                        #
                        # if self.STATUS:
                        #     self.STATUS = False
                        #     t2 = MyTask_Tag.MyTask_Tag(
                        #                                 mes=dta,
                        #                                 lstInput=self.lstinput, lstLock=self.lstLock,
                        #                                 TypeReader=dta[1], host=self.host, Port=self.Port,
                        #                                 input1=self._input1, input2=self._input2,
                        #                                 output1=self._output1, output2=self._output2, Pn532=self.pn532, main=self
                        #                                 )
                        #     threadDkTag = Class_Thread('CTag', t2)
                        #     self.lstThread.append(threadDkTag)
                        #     t2.start()
                        break
                    if dta[1] == 'Cancel':
                        print(dta[1])
                        self.lstLock.acquire()
                        id = dta[2].split('\n')[0]
                        sic1 = {id: 0}
                        Func.UpdateDict(sic1, self.lstinput)
                        self.lstLock.release()

                        break
                        pass
                    if dta[1] == "Fopen\n":
                        self.whileVantay = True
                        self.whileThetu = False
                        for i in self.lstThread:
                            # if i.Name != 'Fopen':
                                # if not self.vantaydangdoc: #
                            i.Object.signal = False
                        self.ClearThread()
                        time.sleep(1)
                        # if self.STATUS:
                        #     self.STATUS = False
                        if len(self.lstThread) == 0:
                            t3 = MyTask_Finger.MyTask_Finger(finger=self.finger, mes=dta, namefileImg="fingerprint.jpg", lstInput=self.lstinput, lstLock=self.lstLock,
                                                                 TypeReader=dta[1].split("\n")[0], input1=self._input1, input2=self._input2, output1=self._output1,
                                                                 output2=self._output2, host=self.host, Port=self.Port, uart=self.uart, main=self
                                                                 )
                            threadOPen = Class_Thread('Fopen', t3)
                            self.lstThread.append(threadOPen)
                            t3.start()
                            break
                    if dta[1] == 'Copen\n':
                        # for i in self.lstThread:
                        #     if i.Set_GetName != 'Copen':
                        #         if not self.Thetudangdoc: #
                        #             i.Thread_.Exit = False
                        #         self.ClearThread()
                        #
                        # if self.STATUS:
                        #     self.STATUS = False
                        #     t21 = MyTask_Tag.MyTask_Tag(
                        #         mes=dta
                        #         , lstInput=self.lstinput, lstLock=self.lstLock
                        #         , TypeReader=dta[1], host=self.host, Port=self.Port,
                        #         input1=self._input1, input2=self._input2,
                        #         output1=self._output1, output2=self._output2, Pn532=self.pn532, main=self
                        #     )
                        #     threadDkTag1 = Class_Thread('Copen', t21)
                        #     self.lstThread.append(threadDkTag1)
                        #     t21.start()

                        break
                    if dta[1] == 'Pused':
                        self.lstLock.acquire()
                        id = dta[2].split('\n')[0]
                        sic1 = {id: 1}
                        Func.UpdateDict(sic1, self.lstinput)
                        self.lstLock.release()
                        try:
                            if int(id) > 16:
                                self._output2[int(id) - 17].value = True
                            else:
                                self._output1[int(id) - 1].value = True
                            t5 = threading.Thread(target=Func.CloseLocker,
                                                  args=[dta, self.host, self.Port, self._output1, self._output2,
                                                        self._input1, self._input2, self.tinhieuchot])
                            t5.start()
                        except Exception as Loi2:
                            print('Loi Chua co Board Io',str(Loi2))
                        break
                    if dta[1] == 'Dooropen':
                        self.lstLock.acquire()
                        id = dta[2].split('\n')[0]
                        sic1 = {id: 0}
                        Func.UpdateDict(sic1, self.lstinput)
                        self.lstLock.release()
                        try:
                            if int(dta[2]) > 16:
                                self._output2[int(dta[2]) - 17].value = True
                            else:
                                self._output1[int(dta[2]) - 1].value = True
                            t6 = threading.Thread(target=Func.OpenLocker,
                                                  args=[dta, self.host, self.Port, self._output1, self._output2])
                            t6.start()
                        except Exception as Loi1:
                            print('Loi Chua co Board Io',str(Loi1))
                        break
                    if dta[1] == 'FDK\n':  # FDK\n
                        self.whileVantay = True
                        self.whileThetu = False

                        for i in self.lstThread:
                            # if i.Name != 'Sig':
                                # if not self.vantaydangdoc: #
                            i.Object.signal = False
                        self.ClearThread()
                        time.sleep(1)
                        # if self.STATUS:
                        #     self.STATUS = False
                        if len(self.lstThread) == 0:
                            Finger_sign = MyTask_Finger.MyTask_Finger(finger=self.finger, mes=dta, namefileImg="fingerprint.jpg",
                                                                          lstInput=self.lstinput, lstLock=self.lstLock, TypeReader=dta[1].split("\n")[0],
                                                                          input1=self._input1, input2=self._input2, output1=self._output1, output2=self._output2,
                                                                          host=self.host, Port=self.Port, uart=self.uart, main=self)
                            threadSig = Class_Thread('Sig', Finger_sign)
                            self.lstThread.append(threadSig)
                            Finger_sign.start()
                            break
                break
            self.condition.wait()
            self.condition.release()
        print('Thread OUT')
    def __del__(self):
        print('Doi Tuong ThreadCMD da bi xoa')
