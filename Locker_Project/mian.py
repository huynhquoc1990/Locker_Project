import time
import serial
import socket
import busio
import digitalio
import board
from adafruit_mcp230xx.mcp23017 import MCP23017

from adafruit_pn532.spi import PN532_SPI
import base64
import threading
from io import BytesIO
from digitalio import DigitalInOut
import Locker_Project.Locker
from Locker_Project import CMD_ScanInput, CMD_Thread, CMD_Process, Func, Locker, adafruit_fingerprint

host='192.168.100.3'
Port=3003
threamain=[]
lstID=[]
lstLocker={}
tinhieuchot=True

lst=['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30']
lstouputtemp = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
lstinputtemp = [7, 6, 5, 4, 3, 2, 1, 0, 11, 10, 9, 8, 15, 14, 13, 12]
lstInput1=[]
lstInput2=[]
lstOutput1=[]
lstOutput2=[]
i2c=busio.I2C(board.SCL,board.SDA)

spi = busio.SPI(board.SCLK, board.MOSI, board.MISO)
cs_pin = DigitalInOut(board.CE0)
reset_pin = DigitalInOut(board.CE1)
pn532 = PN532_SPI(spi, cs_pin, reset=reset_pin,debug=False)

sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

exit_event=threading.Event()

Danhsachtu=[] # chứa và quản lý danh sách tủ
uart = serial.Serial("/dev/ttyS0", baudrate=528000, timeout=1)#489600  528000
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)
def Connect_Device():
    try:
        lstI2C=i2c.scan()
        print(lstI2C)
        if len(pn532.firmware_version)!=4:
            raise RuntimeError('Loi Ket Noi Dau Doc The Tu')
        if(len(lstI2C)!=4):
           raise  RuntimeError('Loi Ket noi Board inout')
        pn532.SAM_configuration()
        mcpOutput1 = MCP23017(i2c, 0x21)
        mcpInput1 = MCP23017(i2c, 0x26)

        mcpOutput2 = MCP23017(i2c, 0x20)
        mcpInput2 = MCP23017(i2c, 0x27)

        KhaiBaoInput(mcpInput1,mcpInput2)
        KhaiBaoOutput(mcpOutput1,mcpOutput2)

        if len(lstI2C)!=4:
            raise RuntimeError('Loi ket noi I2C')
        if finger.read_templates() != adafruit_fingerprint.OK:
            raise RuntimeError("Failed to read templates")
        #print("Fingerprint templates: ", finger.templates)
        if finger.count_templates() != adafruit_fingerprint.OK:
            raise RuntimeError("Failed to read templates")
        #print("Number of templates found: ", finger.template_count)
        if finger.read_sysparam() != adafruit_fingerprint.OK:
            raise RuntimeError("Failed to get system parameters")
    except Exception as e:
        print('Error: ',str(e))

def KhaiBaoInput(mcpInput1,mcpInput2):
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
def KhaiBaoOutput(mcpOutput1,mcpOutput2):
    for i in lstouputtemp:
        pin1 = mcpOutput1.get_pin(i)
        pin1.switch_to_output(value=False)
        lstOutput1.append(pin1)
        pin2 = mcpOutput2.get_pin(i)
        pin2.switch_to_output(value=False)
        lstOutput2.append(pin2)
        pass
    pass
def Get_Finger_Image(signak=True):
    """Scan fingerprint then save image to filename."""
    times=time.time()
    check=False
    try:
        while ((time.time()-times<=5) and signak==True):
            i = finger.get_image()
            if i == adafruit_fingerprint.OK:
                check=True
                break
            if i == adafruit_fingerprint.NOFINGER:
                print(".", end="", flush=True)
            elif i == adafruit_fingerprint.IMAGEFAIL:
                print("Imaging error")
                return False
            else:
                print("Other error")
                return False
        if check==False:
            return False
        # let PIL take care of the image headers and file structure
        from PIL import Image  # pylint: disable=import-outside-toplevel
        img= Image.new("L", (256, 288), "white")#256, 288
        pixeldata = img.load()
        mask = 0b00001111
        result = finger.get_fpdata(sensorbuffer="image")
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
        img.save(buffer,format="PNG") #Enregistre l'image dans le buffer
        myimage = buffer.getvalue()
        return base64.b64encode(myimage).decode('utf-8')
    except Exception as e:
        print('Loi Doc Van Tay',str(e))
        # sensor_reset()
        return False
    pass


def Run():
    try:
        Connect_Device()
        chuoi = '<id>1212</id><type>getdata</type><data>statusdoor</data>'
        chuoi = chuoi.encode('utf-8')
        size = len(chuoi)
        while 1:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as scok112:
                    scok112.connect((host, Port))
                    scok112.sendall(size.to_bytes(4, byteorder='big'))
                    scok112.sendall(chuoi)
                    msg = scok112.recv(1024)
                    dta = msg.decode('utf-8')
                    id = dta.split(';')[0]
                    ref = dta.split(';')[1].split('\n')[0].split('/')
                    print(ref)
                    if id == '1212':
                        lstLocker = Func.Convert1(ref)
                        print(lstLocker)
                    scok112.close()
                    #
                    # for i in lstLocker.items():
                    #     tu=Locker.Locker(Id=i[0],Status=i[1],Sign='')
                    #     Danhsachtu.append(tu)
                    # print(Danhsachtu)
                    break
            except Exception as e:
                scok112.close()
                print('Loi Roi')
        time.sleep(2)

        condition=threading.Condition()
        lstLock=threading.Lock()

        producer=CMD_Thread.Producer(Cmd=lstID,condition=condition,host=host,Port=Port,exitEvent=exit_event)
        threamain.append(producer)

        fingerT=CMD_Process.CMD_Process(finger=finger,pn532=pn532, Cmd=lstID,condition=condition,
                                        lst_input=lstLocker,lstLock=lstLock,
                                        exitEvent=exit_event,input1=lstInput1,
                                        input2=lstInput2,output1=lstOutput1,output2=lstOutput2,
                                        tinhieuchot=tinhieuchot,host=host,Port=Port)
        threamain.append(fingerT)
        scan = CMD_ScanInput.ScanInput(lstinput=lstLocker, lstlock=lstLock,
                                       lstID=lst,exitEvent=exit_event,
                                       input1=lstInput1,input2=lstInput2,
                                       output1=lstOutput1,output2=lstOutput2)
        threamain.append(scan)
        for t in threamain:
            t.start()

        #print('Xuong roi ne')
        #exit_event.set()

    except Exception as e:
        print('Connect Mysql Error:',str(e))