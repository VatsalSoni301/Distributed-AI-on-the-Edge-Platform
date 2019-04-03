from datetime import datetime  
myFile = open('append.txt', 'a')  
myFile.write('\nAccessed on ' + str(datetime.now()))  
