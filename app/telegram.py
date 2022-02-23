
import os
import secrets
import requests

def sendText(botMessage, debug):
   apiUrl = "https://api.telegram.org/bot" + secrets.botToken + "/sendMessage?chat_id=" + secrets.botChatID + "&parse_mode=Markdown&text=" + botMessage

   if debug:
      print(botMessage)
   else:
      response = requests.get(apiUrl)
      return response.json()


def handleFile(filePath):
   print(__file__)
   with open(filePath, 'r') as f:
      message = f.read()
      sendText(message, False)
      os.remove(filePath)
      print("SENT:\n" + message)
  

#test = sendText("Sää on talvinen.")
#print(test)

path = os.path.dirname(os.path.realpath('__file__'))
dirPath = path + "/data/"


# For all files  
for file in os.listdir(dirPath):
    if file.endswith(".txt"):
        filePath = dirPath + file
  
        handleFile(filePath)
