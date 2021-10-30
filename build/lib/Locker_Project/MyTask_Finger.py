import base64
import socket
import threading
import time
from io import BytesIO
from Locker_Project import Func
from Locker_Project import adafruit_fingerprint
from PIL import Image
import ctypes


class MyTask_Finger(threading.Thread):

    def __init__(self, finger, namefileImg, lstInput, lstLock, host,
                 Port, input1, input2, output1, output2, uart, main):
        threading.Thread.__init__(self)
        self.uart = uart
        self.finger = finger
        self.namefileImg = namefileImg
        self.lstInput = lstInput
        self.listLock = lstLock
        self.host = host
        self.Port = Port
        self._input1 = input1
        self._input2 = input2
        self._output1 = output1
        self._output2 = output2
        self.processMain = main

    mes = None
    TypeRead = None

    def Get_Finger_Image(self):
        times = time.time()
        try:
            while time.time() - times <= 30:  # Ham kich hoat cam bien van tay
                i = self.finger.get_image()
                if i == adafruit_fingerprint.OK:
                    times1 = time.time()
                    img = Image.new("L", (256, 288), "white")  # 256, 288
                    pixeldata = img.load()
                    mask = 0b00001111

                    # đoạn này bắt đầu đẩy dữ liệu tù cảm biến vân tay lên cho con Rasp pi Zero
                    result = self.finger.get_fpdata(sensorbuffer="image")
                    x = 0
                    y = 0
                    for i in range(len(result)):
                        pixeldata[x, y] = (int(result[i]) >> 4) * 17
                        x += 1
                        pixeldata[x, y] = (int(result[i]) & mask) * 17
                        if x == 255:
                            x = 0
                            y += 1
                        else:
                            x += 1
                    buffer = BytesIO()
                    img.save(buffer, format="PNG")  # Enregistre l'image dans le buffer
                    myimage = buffer.getvalue()
                    print(f'Gia tri doc cam bien = {time.time() - times1}')
                    return base64.b64encode(myimage).decode('utf-8')
        except Exception as e:
            print('Loi Van Tay', str(e))
        finally:
            print('Hoàn thành thread Đoc vân tay')

    def run(self):
        try:
            damage = self.Get_Finger_Image()
            if damage is None or damage is False:
                print('khong co hinh anh')
                return False
            elif len(self.mes) == 2:
                Id, value1 = [i for i in self.mes]
                if self.TypeRead == 'FDK':
                    dta1 = Func.TaiCauTruc(Id, value1, damage)
                    dta2 = bytes(dta1, 'utf-8')
                    size = len(dta2)
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sck:
                        sck.connect((self.host, self.Port))
                        sck.sendall(size.to_bytes(4, byteorder='big'))
                        sck.sendall(dta2)
                        sck.close()
                        del damage, dta1
                    pass
                elif self.TypeRead == 'Fopen':
                    dta1 = bytes(Func.TaiCauTruc(Id, 'Fopen', damage), 'utf-8')
                    size = len(dta1)
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                        sock.connect((self.host, self.Port))
                        sock.sendall(size.to_bytes(4, byteorder='big'))
                        sock.sendall(dta1)
                        del dta1
            elif len(self.mes) == 3:
                Id, typevalue, value = [i for i in self.mes]
                if self.TypeRead == 'Fused':
                    dta1 = bytes(Func.TaiCauTruc(Id, 'Fused', damage), 'utf-8')
                    size = len(dta1)
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock1:
                        sock1.connect((self.host, self.Port))
                        sock1.sendall(size.to_bytes(4, byteorder='big'))
                        sock1.sendall(dta1)
                        del dta1
        except Exception as e:
            print('Loi Roi', str(e))
        finally:
            print('Ket thuc thread', self.name)
            self.processMain.ThreadFinger.ThreadName = 'th'

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

    def __del__(self):
        print(self.name, 'thread myTag_Finger bi Xoa')
