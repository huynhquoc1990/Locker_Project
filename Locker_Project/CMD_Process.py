import threading

from Locker_Project import Locker,Func,MyTask_Finger,MyTask_Tag,Test_Send_Dta

class CMD_Process(threading.Thread):
    exit_event=threading.Event()
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
                            t10=threading.Thread(target=Func.CloseLocker,args=[self.mes,self.host,self.Port,self._output1,self._output2,self._input1,self._input2,self._tinhieuchot])
                            t10.start()
                            break
                        if (dta[1]=='Fused' and dta[2]!="OK\n"):
                            try:
                                if len(self.ListThread)>0:
                                    k=0
                                    for i in self.ListThread:
                                        i.Exit=False
                                        try:
                                            self.ListThread.pop(k)
                                        except Exception as e:
                                            print(str(e))
                                        k+=1
                                t1=MyTask_Finger.MyTask_Finger(finger=self.finger,mes=dta,
                                                               namefileImg="fingerprint.jpg", lstInput=self.lstinput,
                                                               lstLock=self.lstLock, TypeReader=dta[1],
                                                               input1=self._input1,  input2=self._input2,
                                                               output1=self._output1,output2=self._output2,
                                                               host=self.host,Port=self.Port, tinhieuchot=self.tinhieuchot,uart=self.uart)

                                self.ListThread.append(t1)
                                print(len(self.ListThread))
                                t1.start()
                                break
                                # t1.join()
                            except Exception as e:
                                #self._blynk.notify('Fused Error: '+ str(e))
                                print('0',str(e))
                        if ((dta[1]=='Cused') and dta[2]!="OK\n"):
                            try:
                                if len(self.ListThread)>0:
                                    k=0
                                    for i in self.ListThread:

                                        i.Exit=False
                                        try:
                                            self.ListThread.pop(k)
                                        except Exception as e:
                                            print(str(e))
                                        k+=1
                                t2=MyTask_Tag.MyTask_Tag(
                                    mes=dta
                                    ,lstInput=self.lstinput,lstLock= self.lstLock
                                    ,TypeReader= dta[1], host=self.host, Port=self.Port,
                                    input1=self._input1, input2=self._input2,
                                    output1=self._output1, output2=self._output2, tinhieuchot=self.tinhieuchot,Pn532=self.pn532
                                    )
                                self.ListThread.append(t2)
                                print(len(self.ListThread))
                                t2.start()
                                break
                                # t2.join()
                            except Exception as e:
                                #self._blynk.notify('Cused Error: ' + str(e))
                                print('1',str(e))
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
                            try:
                                if len(self.ListThread)>0:
                                    k=0
                                    for i in self.ListThread:
                                        i.finger.close_uart()
                                        i.Exit=False
                                        try:
                                            self.ListThread.pop(k)
                                        except Exception as e:
                                            print(str(e))
                                        k+=1
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
                                                               tinhieuchot=self.tinhieuchot,uart=self.uart)
                                self.ListThread.append(t3)
                                print(len(self.ListThread))
                                t3.start()
                                break
                                # t3.join()
                            except Exception as e:
                                #self._blynk.notify('Fopen Error: ' + str(e))
                                print('2',str(e))
                        if (dta[1]=='Copen\n'):
                            try:
                                if len(self.ListThread)>0:
                                    k=0
                                    for i in self.ListThread:
                                        i.Exit=False
                                        try:
                                            self.ListThread.pop(k)
                                        except Exception as e:
                                            print(str(e))
                                        k+=1
                                t4=MyTask_Tag.MyTask_Tag(
                                    mes=dta,
                                    lstInput= self.lstinput,
                                    lstLock= self.lstLock,
                                    TypeReader= dta[1].split("\n")[0],
                                    host=self.host,Port=self.Port,
                                    input1=self._input1,input2=self._input2,
                                    output1=self._output1,output2=self._output2,tinhieuchot=self.tinhieuchot,Pn532=self.pn532
                                    )
                                self.ListThread.append(t4)
                                print(len(self.ListThread))
                                t4.start()
                                break
                                #t4.join()
                            except Exception as e:
                                #self._blynk.notify('Copen Error: ' + str(e))
                                print(str(e))
                        if (dta[1]=='Pused'):
                            print(dta[1])
                            try:
                                if len(self.ListThread)>0:
                                    k=0
                                    for i in self.ListThread:
                                        i.Exit=False
                                        try:
                                            self.ListThread.pop(k)
                                        except Exception as e:
                                            print(str(e))
                                        k+=1
                                self.lstLock.acquire()
                                id=dta[2].split('\n')[0]
                                sic1={id:1}
                                Func.UpdateDict(sic1,self.lstinput)
                                self.lstLock.release()
                                #self._blynk.notify('Tu {} Duoc Kich Hoat su Dung'.format(id))
                                if int(id)>16:
                                    self._output2[int(id)-17].value=True
                                else:
                                    self._output1[int(id)-1].value=True
                                t5=threading.Thread(target=Func.CloseLocker,args=[dta,self.host,self.Port,self._output1,self._output2,self._input1,self._input2,self.tinhieuchot])
                                t5.start()
                                break
                            except Exception as e:
                                #self._blynk.notify('Pused Error: ' + str(e))
                                print(str(e))
                        if dta[1]=='Dooropen':
                            print(dta[1])
                            try:
                                if len(self.ListThread)>0:
                                    k=0
                                    for i in self.ListThread:
                                        i.Exit=False
                                        try:
                                            self.ListThread.pop(k)
                                        except Exception as e:
                                            print(str(e))
                                        k+=1
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
                            except Exception as e:
                                #self._blynk.notify('Dooropen Error: ' + str(e))
                                print(str(e))
                        if dta[1]=='FDK\n':#FDK\n
                            if len(self.ListThread)>0:
                                k=0
                                for i in self.ListThread:
                                    i.Exit=False
                                    try:
                                        self.ListThread.pop(k)
                                    except Exception as e:
                                        print(str(e))
                                    k+=1
                            Finger_sign=MyTask_Finger.MyTask_Finger(finger=self.finger
                                                                ,mes=dta,namefileImg="fingerprint.jpg",
                                                               lstInput= self.lstinput,lstLock= self.lstLock,TypeReader= dta[1].split("\n")[0],
                                                               input1=self._input1,input2=self._input2,output1=self._output1, output2=self._output2,
                                                               host=self.host,Port=self.Port,tinhieuchot=self.tinhieuchot,uart=self.uart)
                            self.ListThread.append(Finger_sign)
                            Finger_sign.start()
                            break
                        break
                    except Exception as e:
                        print('Main Erro: ',str(e))

                self.condition.wait()
            self.condition.release()
    def __del__(self):
        print('Doi Tuong ThreadCMD da bi xoa')
