
class Locker:
    def __init__(self,Id,Status,Signal_Input=False,Signal_Output=False):
        self._Id=Id
        self._Status=Status
        self._Signal_Input=Signal_Input
        self._Signal_Output=Signal_Output
    @property
    def Sigin(self):
        return self._Sign

    @Sigin.setter
    def Sigin(self,sign):
        self._Sign=sign

    @property
    def Status(self):
        return self._Status
    @Status.setter
    def Status(self,staus):
        self._Status=staus

    def Open_Locker(self):

        pass

    def Closs_Locker(self):

        pass
    def __del__(self):
        print('Locker Deleted')
