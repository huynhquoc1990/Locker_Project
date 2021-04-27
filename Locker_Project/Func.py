import base64
import socket
import subprocess
import time
from io import BytesIO

from Locker_Project import adafruit_fingerprint


def TaiCauTruc(_Id,_TypeId,_Data,GetData=1):
    if GetData==1:
        return f'<id>{_Id}</id><type>{_TypeId}</type><data>{_Data}</data>'
    elif GetData==2:
        return f'<id>{_Id}</id><type>Doorclose</type><data>{_Data}</data>'
    elif GetData==3:
        return f'<id>{_Id}</id><type>Dooropen</type><data>{_Data}</data>'
    else:
        return f"<id>Error</id><type>{_TypeId}</type><data>{_Data}</data>"
    pass

def get_base64_encoded_image(image_path):
    with open(image_path,"rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    pass

def shut_down():
    print ("shutting down")
    command = "/usr/bin/sudo /sbin/shutdown -h now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print (output)

def UpdateDict(dictupdate,di):
    di.update(dictupdate)
    pass

def Convert1(lst):
	dict1={lst[i].split(':')[0]:int(lst[i].split(':')[1]) for i in range(0,len(lst)-1)}
	return dict1

def restart():
    print ("restarting Pi")
    command = "/usr/bin/sudo /sbin/shutdown -r now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print (output)
    pass

def sensor_reset(finger):
    """Reset sensor"""
    print("Resetting sensor...")
    if finger.soft_reset() != adafruit_fingerprint.OK:
        print("Unable to reset sensor!")
    print("Sensor is reset.")
'''Lấy ảnh image từ finger, mặc định được lấy về ảnh có định dạng jpg'''
def Get_Finger_Image(finger,signak=True):
    """Scan fingerprint then save image to filename."""
    times=time.time()
    check=False
    try:
        while ((time.time()-times<=3) and signak==True):
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

        print(result)
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
        sensor_reset()
        return False
def OpenLocker(*args):
    try:
        id,typeF,value=[i for i in args[0]]
        host=args[1]
        Port=args[2]
        lstOutput1=args[3]
        lstOutput2=args[4]
        demtime=time.time()
        time.sleep(2)
        if int(value)>16:
            with socket.socket(socket.AF_INET,socket.SOCK_STREAM)as Sok:
                Sok.connect((host,Port))
                lstOutput2[int(value)-17].value=False
                dtan=bytes(TaiCauTruc(id,'Dooropen',value.split("\n")[0],GetData=3),'utf-8')
                Sok.sendall(len(dtan).to_bytes(4,'big'))
                Sok.sendall(dtan)
                Sok.close()
        else:
            with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as Sok:
                Sok.connect((host,Port))
                lstOutput1[int(value)-1].value=False
                dtan=bytes(TaiCauTruc(id,'Dooropen',value.split("\n")[0],GetData=3),'utf-8')
                Sok.sendall(len(dtan).to_bytes(4,'big'))
                Sok.sendall(dtan)
                Sok.close()
    except Exception as e:
        print('OpenLocker=:',str(e))
        pass
    pass

def CloseLocker(*args):
    try:
        id,ty,loker=[i for i in args[0]]
        host = args[1]
        Port = args[2]
        lstOutput1 = args[3]
        lstOutput2 = args[4]
        lstInput1=args[5]
        lstInput2=args[6]
        tinhieuchot=args[7]

        demtime=time.time()
        time.sleep(2)
        while time.time()-demtime<=30:# chờ tín hiệu dong cua ne: Chờ 3 phut =180s
            if int(loker)>16:
                lstOutput2[int(loker)-17].value=False
                if lstInput2[int(loker)-17].value==tinhieuchot:

                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as Sok:
                        Sok.connect((host, Port))
                        dtan=bytes(TaiCauTruc(id,'Doorclose',loker.split("\n")[0],GetData=2),'utf-8')
                        Sok.sendall(len(dtan).to_bytes(4,'big'))
                        Sok.sendall(dtan)
                        Sok.close()
                        break
            else:
                lstOutput1[int(loker)-1].value=False
                if lstInput1[int(loker)-1].value==tinhieuchot:

                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as Sok:
                        Sok.connect((host, Port))
                        dtan=bytes(TaiCauTruc(id,'Doorclose',loker.split("\n")[0],GetData=2),'utf-8')
                        Sok.sendall(len(dtan).to_bytes(4,'big'))
                        Sok.sendall(dtan)
                        Sok.close()
                        break
            time.sleep(1)
    except Exception as e:
        print('CloseLocker :',str(e))
    pass