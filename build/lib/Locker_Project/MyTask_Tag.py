import ctypes
import socket
import threading
import time
from Locker_Project import Func


class MyTask_Tag(threading.Thread):
    signal = True
    mes = None
    TypeRead = None

    def __init__(self, lstInput, lstLock, host, Port, input1, input2, output1, output2, Pn532, main):
        threading.Thread.__init__(self)
        self.lstInput = lstInput
        self.listLock = lstLock
        self.host = host
        self.Port = Port
        self._input1 = input1
        self._input2 = input2
        self._output1 = output1
        self._output2 = output2
        self._Reader = Pn532
        self.processMain = main

    def get_id(self):
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for iD, thread in threading._active.items():
            if thread is self:
                return iD

    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')

    def run(self):
        try:
            valueTag = ''
            times = time.time()
            check = False

            while time.time() - times <= 30:
                uid = self._Reader.read_passive_target(timeout=0.5)
                if uid is not None:
                    valueTag = ''.join([hex(i) for i in uid])
                    check = True
                    break
                self._Reader.power_down()

            if check:
                if len(self.mes) == 2:
                    Id, value1 = [i for i in self.mes]
                    if self.TypeRead == 'Copen':
                        dta1 = bytes(Func.TaiCauTruc(Id, 'Copen', valueTag), 'utf-8')
                        size = len(dta1)
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                            sock.connect((self.host, self.Port))
                            sock.sendall(size.to_bytes(4, byteorder='big'))
                            sock.sendall(dta1)
                            sock.close()
                            del dta1
                elif len(self.mes) == 3:
                    Id, typevalue, value = [i for i in self.mes]
                    if self.TypeRead == 'Cused':
                        dta1 = bytes(Func.TaiCauTruc(Id, typevalue, valueTag), 'utf-8')
                        size = len(dta1)
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock11:
                            sock11.connect((self.host, self.Port))
                            sock11.sendall(size.to_bytes(4, byteorder='big'))
                            sock11.sendall(dta1)
                            del dta1
        finally:
            self.processMain.ThreadTag.ThreadName = 'th'
            print('Hoan thành Thread Thẻ Từ', self.name)

    def __del__(self):
        print(self.name, ' Đã bị xóa')
