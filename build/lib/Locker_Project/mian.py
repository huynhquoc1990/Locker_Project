import struct
import time
import board
import serial
import socket
import busio
import digitalio

from adafruit_mcp230xx.mcp23017 import MCP23017
from adafruit_pn532.spi import PN532_SPI
# import base64
import threading
# from io import BytesIO
from digitalio import DigitalInOut
from Locker_Project import CMD_Thread, CMD_Process, Func, adafruit_fingerprint

host = ''
Port = 3003
threamain = []
lstID = []
lstLocker = {}
tinhieuchot = False

lst = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
       '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30']
lstouputtemp = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
# lstinputtemp = [7, 6, 5, 4, 3, 2, 1, 0, 11, 10, 9, 8, 15, 14, 13, 12] // dia chi IO board ngoài anh Hải 24Vdc

lstinputtemp = [7, 6, 5, 4, 3, 2, 1, 0, 15, 14, 13, 12, 11, 10, 9, 8]

lstInput1 = []
lstInput2 = []
lstOutput1 = []
lstOutput2 = []

i2c = busio.I2C(board.SCL, board.SDA)

spi = busio.SPI(board.SCLK, board.MOSI, board.MISO)
cs_pin = DigitalInOut(board.CE0)
reset_pin = DigitalInOut(board.CE1)
try:
    pn532 = PN532_SPI(spi, cs_pin, reset=reset_pin, debug=False)
except:
    pn532 = None
    
exit_event = threading.Event()

Danhsachtu = []  # chứa và quản lý danh sách tủ
uart = serial.Serial("/dev/ttyAMA0", baudrate=528000, timeout=1)
try:
    finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)
    print('Van tay tim thay')
except Exception as e:
    print('Khoi tao Van Tay bị Lỗi', str(e))
    finger = None


def Connect_Device():
    try:
        lstI2C = i2c.scan()
        print(lstI2C)
        if len(pn532.firmware_version) != 4:
            print('Loi Ket Noi Dau Doc The Tu')
            return False
        if len(lstI2C) != 4:
            print('Loi Ket noi Board inout')
            return False
        pn532.SAM_configuration()
        mcpOutput1 = MCP23017(i2c, 0x26)
        mcpOutput2 = MCP23017(i2c, 0x27)

        mcpInput1 = MCP23017(i2c, 0x20)
        mcpInput2 = MCP23017(i2c, 0x21)

            # mcpOutput1 = MCP23017(i2c, 0x21)
            # mcpInput1 = MCP23017(i2c, 0x26)
            #
            # mcpOutput2 = MCP23017(i2c, 0x27)  # board 2 cuar Mr Hai
            # mcpInput2 = MCP23017(i2c, 0x20)  # board 2 cuar Mr Hai
            # mcpOutput2 = MCP23017(i2c, 0x20)
            # mcpInput2 = MCP23017(i2c, 0x27)

        KhaiBaoInput(mcpInput1, mcpInput2)
        KhaiBaoOutput(mcpOutput1, mcpOutput2)

        if len(lstI2C) != 4:
            print('Loi ket noi I2C')
            return False
        if finger.read_templates() != adafruit_fingerprint.OK:
            print("Failed to read templates")
            return False
        # print("Fingerprint templates: ", finger.templates)
        if finger.count_templates() != adafruit_fingerprint.OK:
            print("Failed to read templates")
            return False
        # print("Number of templates found: ", finger.template_count)
        if finger.read_sysparam() != adafruit_fingerprint.OK:
            print("Failed to get system parameters")
            return False
        return True
    except Exception as e:
        print('Error: ', str(e))
        return False


def KhaiBaoInput(mcpInput1, mcpInput2):
    for i in lstinputtemp:
        pin = mcpInput1.get_pin(i)
        pin.direction = digitalio.Direction.INPUT
        pin.pull = digitalio.Pull.UP
        lstInput1.append(pin)
        pin1 = mcpInput2.get_pin(i)
        pin1.direction = digitalio.Direction.INPUT
        pin1.pull = digitalio.Pull.UP
        lstInput2.append(pin1)
        pass
    pass


def KhaiBaoOutput(mcpOutput1, mcpOutput2):
    for i in lstouputtemp:
        pin1 = mcpOutput1.get_pin(i)
        pin1.switch_to_output(value=False)
        lstOutput1.append(pin1)
        pin2 = mcpOutput2.get_pin(i)
        pin2.switch_to_output(value=False)
        lstOutput2.append(pin2)
        pass
    pass


def get_default_gateway_linux():
    """Read the default gateway directly from /proc."""
    with open("/proc/net/route") as fh:
        print(fh)
        for line in fh:
            fields = line.strip().split()
            if fields[1] != '00000000' or not int(fields[3], 16) & 2:
                # If not default route or not RTF_GATEWAY, skip it
                continue
            return socket.inet_ntoa(struct.pack("<L", int(fields[2], 16)))


DemVanTay = 0

version = '0.6.3'

txt = 'Chưa kết nối được ngoại vi'


def Run():
    # global ListLocker
    check = False
    while 1:
        LstIp = Func.get_default_gateway_linux()
        print(LstIp)
        for i in LstIp:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3)
                sock.connect((i, Port))
                Host_Ip = i
                print('tim ra Host_Ip!!!!!!!!!!!!!!!!!!', Host_Ip)
                threadmain = '<id>121</id><type>socket</type><data>main</data>'
                threadmain = threadmain.encode('utf-8')
                size1 = len(threadmain)
                sock.sendall(size1.to_bytes(4, byteorder='big'))
                sock.sendall(threadmain)
                time.sleep(1)

                chuoi1 = '<id>12121</id><type>message</type><data>Phần cứng 1.1.2</data>'
                chuoi1 = chuoi1.encode('utf-8')
                size2 = len(chuoi1)
                sock.sendall(size2.to_bytes(4, byteorder='big'))
                sock.sendall(chuoi1)
                time.sleep(1)
                print('1.1.0')

                chuoi2 = '<id>1212</id><type>getdata</type><data>statusdoor</data>'
                chuoi2 = chuoi2.encode('utf-8')
                size2 = len(chuoi2)
                sock.sendall(size2.to_bytes(4, byteorder='big'))
                sock.sendall(chuoi2)
                time.sleep(1)

                msg = sock.recv(1024)
                print(msg)
                dta = msg.decode('utf-8')
                Id = dta.split(';')[0]
                ref = dta.split(';')[1].split('\n')[0].split('/')
                if Id == '1212':
                    ListLocker = Func.Convert1(ref)
                    print(ListLocker)
                print('Goi version Ok')
                check = True
                break
            except Exception as e2:
                print(str(e2))
                sock.close()
                check = False
                break
        if check:
            break
        pass
    dem = 0
    while not Connect_Device():
        print('Chưa kết nối được các thiết bị ngoại vi')
        dem += 1
        time.sleep(1)
        if dem >= 3:
            break
        pass

    condition = threading.Condition()
    lstLock = threading.Lock()

    producer = CMD_Thread.Producer(Cmd=lstID, condition=condition, host=Host_Ip, Port=Port, exitEvent=exit_event,
                                   lstthreadStop=threamain)
    threamain.append(producer)

    fingerT = CMD_Process.Cmd_Process(finger=finger, pn532=pn532, Cmd=lstID, condition=condition,
                                      lst_input=ListLocker, lstLock=lstLock,
                                      exitEvent=exit_event, input1=lstInput1,
                                      input2=lstInput2, output1=lstOutput1, output2=lstOutput2,
                                      host=Host_Ip, Port=Port, uart=uart, tinhieuchot=tinhieuchot)
    threamain.append(fingerT)

    for t in threamain:
        t.start()
        time.sleep(1)


try:
    if __name__ == '__main__':
        Run()
except Exception as e:
    print(str(e))

