def checkUUID(uuid):
    if(len(uuid) != 18):
        return False
    if(uuid.isnumeric()):
        return True
    return False    