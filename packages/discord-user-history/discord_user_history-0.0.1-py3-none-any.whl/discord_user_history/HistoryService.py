import requests, datetime, time
from User import User

class HistoryService:
    def __init__(self, token):
        self.token = token

    def getUser(self, uuid):
        if len(uuid) <= 10:
            return -1
        
        result = requests.get("http://iampekka058.bplaced.net/getUser.php?token={token}&uuid={uuid}".format(token=self.token, uuid=uuid))
        
        return User(text=result.content.decode())

    def existsUser(self, uuid):
        if len(uuid) <= 10:
            return -1

        result = requests.get("http://iampekka058.bplaced.net/getUser.php?token={token}&uuid={uuid}".format(token=self.token, uuid=uuid))
        
        if(result.content == "NO USER"):
            return False
        else:
            return True

    def createUser(self, uuid, profile_id, profile_name):
        if len(uuid) <= 10:
            return -1
        if profile_id == None or profile_id == "":
            return -2
        if profile_name == None or profile_name == "":
            return -3

        requests.get("http://iampekka058.bplaced.net/insert.php?token={}&uuid={}&profile_id={}&profile_name={}&date={}".format(self.token, uuid, profile_id, profile_name, datetime.datetime.today().strftime('%d-%m-%Y, %H:%M:%S')))

    # def getUserHistory(self, uuid):
    #     if len(uuid) <= 10:
    #         return -1
    #     print("Booo")

    def registerChanges(self, uuid, profile_id, profile_name):
        
        # Check if uuid is valid

        if len(uuid) <= 10:
            return -1
        if profile_id == None or profile_id == "":
            return -2
        if profile_name == None or profile_name == "":
            return -3
        
        user = self.getUser(uuid)
        if user.getName() != profile_name or user.getID() != profile_id:
            requests.get("http://iampekka058.bplaced.net/insert.php?token={}&uuid={}&profile_id={}&profile_name={}&date={}".format(self.token, uuid, profile_id, profile_name, datetime.datetime.today().strftime('%d-%m-%Y,%H:%M:%S')))
            name = user.getName()
            id = user.getID()
            requests.get("http://iampekka058.bplaced.net/change.php?token={}&uuid={}&new_id={}&new_name={}&old_id={}&old_name={}&date={}".format(self.token,uuid, profile_id, profile_name, id, name, datetime.datetime.today().strftime('%d-%m-%Y,%H:%M:%S')))
