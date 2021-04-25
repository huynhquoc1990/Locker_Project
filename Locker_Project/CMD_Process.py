import threading

from Locker_Project import Locker,Func

class CMD_Process(threading.Thread):
    def __init__(self,Cmd,condition,lst_input,lstLock,exitEvent):
        threading.Thread.__init__(self)
        self.Cmd=Cmd
        self.condition=condition
        self.ListThread=[]
        self.lstinput=lst_input
        self.lstLock=lstLock
        self._Exit=exitEvent
    @property
    def Exit(self):
        return self._Exit
    @Exit.setter
    def Exit(self,exitEvent):
        self._Exit=exitEvent

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
                            print(dta[1])
                            lock=Locker.Locker()

                            # t1=MyTask_Finger(dta,"fingerprint.jpg",self.lstinput,self.lstLock,dta[1])
                            # self.ListThread.append(t1)
                            # if len(self.ListThread)>0:
                            #     for i in self.ListThread:
                            #         if i.name!=t1.name:
                            #             i.signal=False
                            # t1.start()
                            # t1.join()
                        if ((dta[1]=='Cused') and dta[2]!="OK\n"):
                            print(dta[1])
                            # t2=MyTask_Tag(dta,self.lstinput,self.lstLock,dta[1])
                            #
                            # if len(self.ListThread)>0:
                            #     for i in self.ListThread:
                            #         if i.name!=t2.name:
                            #             i.signal=False
                            #
                            # self.ListThread.append(t2)
                            # t2.start()
                            # t2.join()
                        if (dta[1]=='Cancel'):
                            print(dta[1])
                            # self.lstLock.acquire()
                            # id=dta[2].split('\n')[0]
                            # sic1={id:0}
                            # UpdateDict(sic1,self.lstinput)
                            # self.lstLock.release()
                            # lstOutput1[15].value=True
                            # pass
                        if (dta[1]=='Fopen\n'):#dta[1]=='Fopen\n' or
                            print(dta[1])
                            # t3=MyTask_Finger(dta,"fingerprint.jpg",self.lstinput,self.lstLock,dta[1].split("\n")[0])
                            # self.ListThread.append(t3)
                            # if len(self.ListThread)>0:
                            #     for i in self.ListThread:
                            #         if i.name!=t3.name:
                            #             i.signal=False
                            # t3.start()
                            # t3.join()
                        if (dta[1]=='Copen\n'):
                            print(dta[1])
                            # t4=MyTask_Tag(dta,self.lstinput,self.lstLock,dta[1].split("\n")[0])
                            #
                            # self.ListThread.append(t4)
                            # if len(self.ListThread)>0:
                            #     for i in self.ListThread:
                            #         if i.name!=t4.name:
                            #             i.signal=False
                            # t4.start()
                            # t4.join()
                        if (dta[1]=='Pused'):
                            print(dta[1])
                            try:
                                self.lstLock.acquire()
                                id=dta[2].split('\n')[0]
                                sic1={id:1}
                                Func.UpdateDict(sic1,self.lstinput)
                                self.lstLock.release()
                                if int(id)>16:
                                    lstOutput2[int(id)-17].value=True
                                else:
                                    lstOutput1[int(id)-1].value=True
                                t5=threading.Thread(target=CloseLocker,args=[dta,None])
                                t5.start()
                            except Exception as e:
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
                                    lstOutput2[int(dta[2])-17].value=True
                                else:
                                    lstOutput1[int(dta[2])-1].value=True
                                t6=threading.Thread(target=OpenLocker,args=[dta,None])
                                t6.start()
                            except Exception as e:
                                print(str(e))
                        if dta[1]=='FDK\n':#FDK\n
                            print(dta[1])
                            # if save_fingerprint_image(dta):
                            #     print('finshed')
                            # else:
                            #     print("Failed to save fingerprint image")
                        if dta[1]=='Update\n':

                            pass
                        break
                    except Exception as e:
                        print('Main Erro: ',str(e))
                        # Connect_Device()
                self.condition.wait()
            self.condition.release()
    def __del__(self):
        print('Doi Tuong ThreadCMD da bi xoa')