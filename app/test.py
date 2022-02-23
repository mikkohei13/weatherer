
import os

#path = "/usr/src/app/data"
#path = "./data"
#os.chdir(path)

path = os.path.dirname(os.path.realpath('__file__'))
dirPath = path + "/data/"

def handleFile(filePath):
    print(__file__)
    with open(filePath, 'r') as f:
        print(f.read())
  

# For all files  
for file in os.listdir(dirPath):
    if file.endswith(".txt"):
        filePath = dirPath + file
  
        handleFile(filePath)