import base64
import subprocess
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