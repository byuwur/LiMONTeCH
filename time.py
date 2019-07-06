import time
import os

current=str(time.strftime("%d-%m-%Y"+"_"+"%H-%M-%S"))
print (current)

folderpath="C:/LiMONTECHLogs/"
directory=os.path.dirname(folderpath)

if not os.path.exists(directory):
	os.makedirs(directory)

file = open("C:/LiMONTECHLogs/file_"+current+".txt","w")
file.write("Hello, created file. We're at "+current)
file.close()