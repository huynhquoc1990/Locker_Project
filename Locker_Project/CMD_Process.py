import threading

from Locker_Project import Locker,Func,MyTask_Finger,MyTask_Tag,Test_Send_Dta
class Class_Thread():
    def __init__(self,name,ObjectThread):
        self.Name=name
        self.Object=ObjectThread

    @property
    def Set_GetName(self):
        return self.Name
    @Set_GetName.setter
    def Set_GetName(self,name):
        self.Name=name

    @property
    def Thread_(self):
        return self.Object
    @Thread_.setter
    def Thread_(self,thread):
        self.Object=thread


class CMD_Process(threading.Thread):
    exit_event=threading.Event()
    STATUS=True

    vantaydangdoc=False
    Thetudangdoc=False
    lstThread=[]
    def __init__(self,finger,pn532,Cmd,condition,lst_input,lstLock,exitEvent,input1,input2,output1,output2,host,Port,tinhieuchot,uart):
        threading.Thread.__init__(self)
        self.finger=finger
        self.pn532=pn532
        self.Cmd=Cmd
        self.condition=condition
        self.ListThread=[]
        self.lstinput=lst_input
        self.lstLock=lstLock
        self._Exit=exitEvent
        self._input1=input1
        self._input2 = input2
        self._output1 = output1
        self._output2 = output2
        self.host=host
        self.Port=Port
        self.tinhieuchot=tinhieuchot
        self.uart=uart
        self.dem=0
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

    def ClearThread(self):
        self.lstThread.clear()
        self.STATUS=True

    def run(self):
        temp=''
        while 1:
            if self._Exit.is_set():
                break
            self.condition.acquire()
            while 1:
                print(self.Cmd)
                if len(self.Cmd)>0:
                    dta=self.Cmd.pop().split(";")
                    print('Tramg thai',self.STATUS)
                    # try:
                    if((dta[1]=='Fused' or dta[1]=='Cused') and dta[2]=="OK"):
                        self.lstLock.acquire()
                        id=dta[3].split('\n')[0]
                        print('id=',id)
                        sic1={id:1}
                        Func.UpdateDict(sic1,self.lstinput)
                        self.lstLock.release()
                        #self._blynk.notify("Tu {} duoc kich hoat".format(id))
                        if int(dta[3])>16:
                            self._output2[int(dta[3])-17].value=True
                        else:
                            self._output1[int(dta[3])-1].value=True
                        t10=threading.Thread(target=Func.CloseLocker,args=[dta,self.host,self.Port,self._output1,self._output2,self._input1,self._input2,self.tinhieuchot])
                        t10.start()
                        break
                    if (dta[1]=='Fused' and dta[2]!="OK\n"):
                        for i in self.lstThread:
                            if i.Name!='dk':
                                if self.vantaydangdoc==False or self.Thetudangdoc==False:
                                    i.Object.Exit=False
                                self.ClearThread()

                        if self.STATUS==True:
                            self.STATUS=False
                            t1=MyTask_Finger.MyTask_Finger(finger=self.finger
                                                           ,mes=dta,
                                                           namefileImg="fingerprint.jpg",
                                                           lstInput= self.lstinput,
                                                           lstLock= self.lstLock,
                                                           TypeReader= dta[1].split("\n")[0],
                                                           input1=self._input1,
                                                           input2=self._input2,
                                                           output1=self._output1,
                                                           output2=self._output2,
                                                           host=self.host,
                                                           Port=self.Port,
                                                           tinhieuchot=self.tinhieuchot,uart=self.uart,main=self)
                            threadOPen=Class_Thread('dk',t1)
                            self.lstThread.append(threadOPen)
                            t1.start()
                            break
                    if ((dta[1]=='Cused') and dta[2]!="OK\n"):
                        for i in self.lstThread:
                            if i.Name!='CTag':
                                if self.Thetudangdoc==False or self.vantaydangdoc==False:
                                    i.Object.Exit=False
                                self.ClearThread()
                            pass
                        if self.STATUS==True:
                            self.STATUS=False
                            t2=MyTask_Tag.MyTask_Tag(
                                mes=dta
                                ,lstInput=self.lstinput,lstLock= self.lstLock
                                ,TypeReader= dta[1], host=self.host, Port=self.Port,
                                input1=self._input1, input2=self._input2,
                                output1=self._output1, output2=self._output2, tinhieuchot=self.tinhieuchot,Pn532=self.pn532,main=self
                            )
                            threadDkTag=Class_Thread('CTag',t2)
                            self.lstThread.append(threadDkTag)
                            t2.start()
                        break
                    if (dta[1]=='Cancel'):
                        print(dta[1])
                        self.lstLock.acquire()
                        id=dta[2].split('\n')[0]
                        sic1={id:0}
                        Func.UpdateDict(sic1,self.lstinput)
                        self.lstLock.release()
                        #self._blynk.notify('Tu {} Bi huy'.format(id))
                        break
                        pass
                    if (dta[1]=='Fopen\n'):#dta[1]=='Fopen\n' or
                        for i in self.lstThread:
                            if i.Name!='open':
                                if self.vantaydangdoc==False or self.Thetudangdoc==False:
                                    i.Object.Exit=False
                                self.ClearThread()
                        if self.STATUS==True:
                            self.STATUS=False
                            t3=MyTask_Finger.MyTask_Finger(finger=self.finger
                                                           ,mes=dta,
                                                           namefileImg="fingerprint.jpg",
                                                           lstInput= self.lstinput,
                                                           lstLock= self.lstLock,
                                                           TypeReader= dta[1].split("\n")[0],
                                                           input1=self._input1,
                                                           input2=self._input2,
                                                           output1=self._output1,
                                                           output2=self._output2,
                                                           host=self.host,
                                                           Port=self.Port,
                                                           tinhieuchot=self.tinhieuchot,uart=self.uart,main=self)
                            threadOPen=Class_Thread('open',t3)
                            self.lstThread.append(threadOPen)
                            t3.start()
                        break
                    if (dta[1]=='Copen\n'):
                        for i in self.lstThread:
                            if i.Name!='Otag':
                                if self.Thetudangdoc==False or self.vantaydangdoc==False:
                                    i.Object.Exit=False
                                self.ClearThread()
                            pass
                        if self.STATUS==True:
                            self.STATUS=False
                            t2=MyTask_Tag.MyTask_Tag(
                                mes=dta
                                ,lstInput=self.lstinput,lstLock= self.lstLock
                                ,TypeReader= dta[1], host=self.host, Port=self.Port,
                                input1=self._input1, input2=self._input2,
                                output1=self._output1, output2=self._output2, tinhieuchot=self.tinhieuchot,Pn532=self.pn532,main=self
                            )
                            threadDkTag=Class_Thread('Otag',t2)
                            self.lstThread.append(threadDkTag)
                            t2.start()
                        break
                    if (dta[1]=='Pused'):
                        self.lstLock.acquire()
                        id=dta[2].split('\n')[0]
                        sic1={id:1}
                        Func.UpdateDict(sic1,self.lstinput)
                        self.lstLock.release()
                        if int(id)>16:
                            self._output2[int(id)-17].value=True
                        else:
                            self._output1[int(id)-1].value=True
                        t5=threading.Thread(target=Func.CloseLocker,args=[dta,self.host,self.Port,self._output1,self._output2,self._input1,self._input2,self.tinhieuchot])
                        t5.start()
                        break
                    if dta[1]=='Dooropen':
                        self.lstLock.acquire()
                        id=dta[2].split('\n')[0]
                        sic1={id:0}
                        Func.UpdateDict(sic1,self.lstinput)
                        self.lstLock.release()
                        if int(dta[2])>16:
                            self._output2[int(dta[2])-17].value=True
                        else:
                            self._output1[int(dta[2])-1].value=True
                        t6=threading.Thread(target=Func.OpenLocker,args=[dta,self.host,self.Port,self._output1,self._output2])
                        t6.start()
                        break

                    if dta[1]=='FDK\n':#FDK\n
                        for i in self.lstThread:
                            if i.Name!='Sig':
                                if self.vantaydangdoc==False:
                                    i.Object.Exit=False
                                self.ClearThread()
                        if self.STATUS==True:
                            self.STATUS=False
                            Finger_sign=MyTask_Finger.MyTask_Finger(finger=self.finger
                                                                    ,mes=dta,namefileImg="fingerprint.jpg",
                                                                    lstInput= self.lstinput,lstLock= self.lstLock,TypeReader= dta[1].split("\n")[0],
                                                                    input1=self._input1,input2=self._input2,output1=self._output1, output2=self._output2,
                                                                    host=self.host,Port=self.Port,tinhieuchot=self.tinhieuchot,uart=self.uart,main=self)
                            threadSig=Class_Thread('Sig',Finger_sign)
                            self.lstThread.append(threadSig)
                            Finger_sign.start()
                        break
                break
            self.condition.wait()
            self.condition.release()
    def __del__(self):
        print('Doi Tuong ThreadCMD da bi xoa')
