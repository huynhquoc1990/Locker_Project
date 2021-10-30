import socket
import threading
import time


class Test_Send_Dta(threading.Thread):
    def __init__(self, host, Port, mes):
        threading.Thread.__init__(self)
        self.signal = True
        self.mes = mes
        self.host = host
        self.Port = Port

    def run(self):
        while 1:
            try:
                chuoi = '<id>1253</id><type>message</type><data>' + self.mes + '</data>'
                chuoi = chuoi.encode('utf-8')
                size = len(chuoi)
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.connect((self.host, self.Port))
                    sock.sendall(size.to_bytes(4, byteorder='big'))
                    sock.sendall(chuoi)
                    sock.close()
                    del chuoi
            except Exception as e:
                print(str(e))
                sock.close()
            time.sleep(2)
            pass

    def __del__(self):
        print(self.name, 'Da duoc Delete')

# if dta[1] == 'Fused' and dta[2] != "OK\n":
#                             for i in self.lstThread:
#                                 if i.Name != 'dk': # truong hop thread sap chay khac thread dang chay
#                                     i.Object.signal = False # thoat thread
#                                     self.ClearThread() # xóa Lst
#                             time.sleep(1)
#                             # print('Trang thai van tay',self.VanTayDangDayDuLieu)
#                             if len(self.lstThread) == 0 and not self.VanTayDangDayDuLieu: # tao thred moi
#                                 t1 = MyTask_Finger.MyTask_Finger(finger=self.finger, mes=dta, namefileImg="fingerprint.jpg",
#                                                                  lstInput=self.lstinput, lstLock=self.lstLock,
#                                                                  TypeReader=dta[1].split("\n")[0], input1=self._input1,
#                                                                  input2=self._input2, output1=self._output1,
#                                                                  output2=self._output2, host=self.host,
#                                                                  Port=self.Port, uart=self.uart, main=self)
#                                 threadOPen = Class_Thread('dk', t1)
#                                 self.lstThread.append(threadOPen)
#                                 t1.start()
#                                 break
#                             else:
#
#                         if dta[1] == "Fopen\n":
#                             for i in self.lstThread:
#                                 if i.Name != 'Fopen':
#                                     i.Object.signal = False
#                                     self.ClearThread()
#                             time.sleep(1)
#                             # print('Trang thai van tay',self.VanTayDangDayDuLieu)
#                             if len(self.lstThread) == 0 and not self.VanTayDangDayDuLieu:
#                                 t3 = MyTask_Finger.MyTask_Finger(finger=self.finger, mes=dta, namefileImg="fingerprint.jpg",
#                                                                  lstInput=self.lstinput, lstLock=self.lstLock,
#                                                                  TypeReader=dta[1].split("\n")[0], input1=self._input1,
#                                                                  input2=self._input2, output1=self._output1,
#                                                                  output2=self._output2, host=self.host, Port=self.Port,
#                                                                  uart=self.uart, main=self
#                                                                  )
#                                 threadOPen = Class_Thread('Fopen', t3)
#
#                                 self.lstThread.append(threadOPen)
#                                 t3.start()
#                                 break
#                         if dta[1] == 'FDK\n':  # FDK\n
#                             for i in self.lstThread:
#                                 if i.Name != 'Sig': # nếu khác tên thread dang chay
#                                     i.Object.signal = False # dừng thread đang chạy lại
#                                     self.ClearThread() # xóa khỏi list
#                             time.sleep(1)  # Chờ các thread dừng hẳng
#                             # print('Trang thai van tay',self.VanTayDangDayDuLieu)
#                             if len(self.lstThread) == 0 and not self.VanTayDangDayDuLieu:
#                                 Finger_sign = MyTask_Finger.MyTask_Finger(finger=self.finger, mes=dta,
#                                                                           namefileImg="fingerprint.jpg",
#                                                                           lstInput=self.lstinput, lstLock=self.lstLock,
#                                                                           TypeReader=dta[1].split("\n")[0],
#                                                                           input1=self._input1, input2=self._input2,
#                                                                           output1=self._output1, output2=self._output2,
#                                                                           host=self.host, Port=self.Port, uart=self.uart,
#                                                                           main=self)
#                                 threadSig = Class_Thread('Sig', Finger_sign)
#                                 self.lstThread.append(threadSig)
#                                 Finger_sign.start()
#                                 break