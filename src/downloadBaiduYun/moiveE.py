import imMail
import logging


logging.basicConfig(level=logging.CRITICAL, format='%(asctime)s - %(levelname)s -%(message)s')

class Moive:
    def __init__(self, name, downloadLink, uideBox):
        self.name = name
        self.downloadLink = downloadLink
        self.uideBox = uideBox
        
class Moives:
    def __init__(self):
        self.moives = []
        eBox = imMail.Ebox()
        messages_folder = eBox.messages(folder='downloading')
        for uid, message in messages_folder:
        # Every message is an object with the following keys
            logging.debug(message.subject)
            logging.debug(message.body['plain'][0])
            name = message.subject
            link = message.body['plain'][0]
            self.moives.append(Moive(name, link, uid))
        eBox.logout()
        
    def downloadSuccess(self, moive):
        imMail.moveMailUid(moive.uideBox, 'downloading', 'downloaded')
        
    
    
# mvs = Moives()