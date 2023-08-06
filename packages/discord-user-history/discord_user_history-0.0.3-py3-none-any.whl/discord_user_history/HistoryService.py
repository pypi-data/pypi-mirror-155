import json
import requests, datetime, time
from User import User
from Validation import checkUUID

class HistoryService:
    def __init__(self, token):
        self.token = token

    def getUser(self, uuid):
        if checkUUID(uuid):
            result = requests.get("http://iampekka058.bplaced.net/getUser.php?token={token}&uuid={uuid}".format(token=self.token, uuid=uuid))
            json_object = json.loads(result.content.decode())
            if(json_object['result'] != 1):
                return None
            return User(text=json_object['user'])

    def existsUser(self, uuid):
        if checkUUID(uuid):
            result = requests.get("http://iampekka058.bplaced.net/getUser.php?token={token}&uuid={uuid}".format(token=self.token, uuid=uuid))
            print(result.content)
            json_object = json.loads(result.content.decode())
            
            if(json_object['result'] == 1):
                return True
            return False

    def createUser(self, uuid, discriminator, name):
        if checkUUID(uuid) == False:
            return -1
        if discriminator == None or discriminator == "":
            return -1
        if name == None or name == "":
            return -1

        requests.get("http://iampekka058.bplaced.net/insert.php?token={}&uuid={}&profile_id={}&profile_name={}&date={}".format(self.token, uuid, discriminator, name, datetime.datetime.today().strftime('%d-%m-%Y, %H:%M:%S')))
    
    # def getUserHistory(self, uuid):
    #     if len(uuid) <= 10:
    #         return -1
    #     print("Booo")

    def registerChanges(self, uuid, discriminator, name):        
        self.registerUpdate(uuid=uuid, discriminator=discriminator, name=name)
    
    def registerUpdate(self, uuid, discriminator, name):
        # Check if uuid is valid
        if checkUUID(uuid) == False:
            return -1
        if discriminator == None or discriminator == "":
            return -1
        if name == None or name == "":
            return -1
        user = self.getUser(uuid)
        if(user == None):
            self.createUser(uuid=uuid, discriminator=discriminator, name=name)
            return 0
        if user.getName() != name or user.getID() != discriminator:
            requests.get("http://iampekka058.bplaced.net/insert.php?token={}&uuid={}&profile_id={}&profile_name={}&date={}".format(self.token, uuid, discriminator, name, datetime.datetime.today().strftime('%d-%m-%Y,%H:%M:%S')))
            name = user.getName()
            id = user.getID()
            requests.get("http://iampekka058.bplaced.net/change.php?token={}&uuid={}&new_id={}&new_name={}&old_id={}&old_name={}&date={}".format(self.token,uuid, discriminator, name, id, name, datetime.datetime.today().strftime('%d-%m-%Y,%H:%M:%S')))
