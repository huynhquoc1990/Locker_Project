import socket
import threading


class Test_Send_Dta(threading.Thread):
    def __init__(self, host, Port, mes):
        threading.Thread.__init__(self)
        self.signal = True
        self.mes = mes
        self.host = host
        self.Port = Port

    def run(self):
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
        pass

    def __del__(self):
        print(self.name, 'Da duoc Delete')
