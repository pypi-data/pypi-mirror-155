class User:
    def __init__(self, uuid, name, id):
        self.profile_uuid = uuid
        self.profile_name = name
        self.profile_id = id

    def __init__(self, text):
        self.profile_uuid = text.split("/")[0]
        self.profile_name = text[text.find("/")+1:text.find("#")]
        self.profile_id = text[text.find("#")+1:]

    def getUUID(self):
        return self.profile_uuid
        
    def getName(self):
        return self.profile_name

    def getID(self):
        return self.profile_id