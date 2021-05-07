import threading

from Locker_Project import Locker,Func,MyTask_Finger,MyTask_Tag



class CMD_Process(threading.Thread):
    def __init__(self,finger,pn532,Cmd,condition,lst_input,lstLock,exitEvent,input1,input2,output1,output2,host,Port,tinhieuchot,blynk):
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
        temp=''
        while 1:
            if self._Exit.is_set():
                break
            self.condition.acquire()
            while 1:
                if len(self.Cmd)>0:
                    print(self.Cmd)
                    dta=self.Cmd.pop().split(";")
                    try:
                        if ((dta[1]=='Fused') and dta[2]!="OK\n"):
                            try:
                                t1=MyTask_Finger.MyTask_Finger(finger=self.finger,mes=dta,
                                                               namefileImg="fingerprint.jpg", lstInput=self.lstinput,
                                                               lstLock=self.lstLock, TypeReader=dta[1],
                                                               input1=self._input1,  input2=self._input2,
                                                               output1=self._output1,output2=self._output2,
                                                               host=self.host,       Port=self.Port, tinhieuchot=self.tinhieuchot)

                                self.ListThread.append(t1)
                                if len(self.ListThread)>0:
                                    for i in self.ListThread:
                                        if i.name!=t1.name:
                                            i.signal=False
                                t1.start()
                                t1.join()
                            except Exception as e:
                                self._blynk.notify('Fused Error: '+ str(e))
                                print(str(e))
                        if ((dta[1]=='Cused') and dta[2]!="OK\n"):
                            try:
                                t2=MyTask_Tag.MyTask_Tag(
                                    pn532=self.pn532,mes=dta
                                    ,lstInput=self.lstinput,lstLock= self.lstLock
                                    ,TypeReader= dta[1], host=self.host, Port=self.Port,
                                    input1=self._input1, input2=self._input2,
                                    output1=self._output1, output2=self._output2, tinhieuchot=self.tinhieuchot
                                    )

                                if len(self.ListThread)>0:
                                    for i in self.ListThread:
                                        if i.name!=t2.name:
                                            i.signal=False

                                self.ListThread.append(t2)

                                t2.start()
                                t2.join()
                            except Exception as e:
                                self._blynk.notify('Cused Error: ' + str(e))
                                print(str(e))
                        if (dta[1]=='Cancel'):
                            print(dta[1])
                            self.lstLock.acquire()
                            id=dta[2].split('\n')[0]
                            sic1={id:0}
                            Func.UpdateDict(sic1,self.lstinput)
                            self.lstLock.release()
                            #lstOutput1[15].value=True
                            pass
                        if (dta[1]=='Fopen\n'):#dta[1]=='Fopen\n' or
                            try:
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
                                                               tinhieuchot=self.tinhieuchot)
                                self.ListThread.append(t3)
                                if len(self.ListThread)>0:
                                    for i in self.ListThread:
                                        if i.name!=t3.name:
                                            i.signal=False
                                t3.start()
                                t3.join()
                            except Exception as e:
                                self._blynk.notify('Fopen Error: ' + str(e))
                                print(str(e))
                        if (dta[1]=='Copen\n'):
                            try:
                                t4=MyTask_Tag.MyTask_Tag(
                                    pn532=self.pn532,
                                    mes=dta,
                                    lstInput= self.lstinput,
                                    lstLock= self.lstLock,
                                    TypeReader= dta[1].split("\n")[0],
                                    host=self.host,Port=self.Port,
                                    input1=self._input1,input2=self._input2,
                                    output1=self._output1,output2=self._output2,tinhieuchot=self.tinhieuchot
                                    )
                                self.ListThread.append(t4)
                                if len(self.ListThread)>0:
                                    for i in self.ListThread:
                                        if i.name!=t4.name:
                                            i.signal=False
                                t4.start()
                                t4.join()
                            except Exception as e:
                                self._blynk.notify('Copen Error: ' + str(e))
                                print(str(e))
                        if (dta[1]=='Pused'):
                            print(dta[1])
                            try:
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
                            except Exception as e:
                                self._blynk.notify('Pused Error: ' + str(e))
                                print(str(e))
                        if dta[1]=='Dooropen':
                            print(dta[1])
                            try:
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
                            except Exception as e:
                                self._blynk.notify('Dooropen Error: ' + str(e))
                                print(str(e))
                        if dta[1]=='FDK\n':#FDK\n
                            print(dta[1])
                            if Func.save_fingerprint_image(dta,self.host,self.Port,self.finger):
                                print('finshed')
                                self._blynk.notify('Dang ky van tay moi thanh cong')
                            else:
                                print("Failed to save fingerprint image")
                                self._blynk.notify('Failed to save fingerprint image')
                        break
                    except Exception as e:
                        print('Main Erro: ',str(e))
                        self._blynk.notify('Main Erro: '+str(e))
                        # Connect_Device()
                self.condition.wait()
            self.condition.release()
    def __del__(self):
        print('Doi Tuong ThreadCMD da bi xoa')
        self._blynk.notify('Doi Tuong ThreadCMD da bi xoa')