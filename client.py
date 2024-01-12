import os
import sys
import socket

#amount of bytes to be read in per loop
packetSize = 4096

#host and port number to make connection to
HOST = str(sys.argv[1])
PORT = int(sys.argv[2])

#request to make to server
requestType = str(sys.argv[3])

#create client socket
cliSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#connect socket to port that host is bound to
cliSock.connect((HOST, PORT))
print(f"Connected to {HOST}-{PORT}.")

def download(filename):


    try:

        #send request to server for it to upload to client
        cliSock.send(f"serverPut {filename}".encode())

        filename = cliSock.recv(packetSize).decode()
        #strip filename down to it's basename
        filename = os.path.basename(filename)

        #check if identical filename already exists
        #disallow overwrite
        if filename in os.listdir():
            print("Error: Cannot overwrite existing file")
            return

        #process of receiving and writing data from file into new file
        with open(filename, "wb") as f:
            while True:
                bytesRead = cliSock.recv(packetSize)
                if len(bytesRead) == 0:
                    break
                f.write(bytesRead)

            cliSock.close()
            print(f"{HOST}-{PORT}: Received file {filename} successfully")

    #if for any reason file could not be received print an error message
    except:
        print(f"{HOST}-{PORT}: Could not receive {filename}")



def upload(filename):
    try:

        #process of sending data to the server
        with open(filename, "rb") as f:

            #have this inside so if file doesn't exist
            #then a filename with no data is not sent to server
            cliSock.send(f"serverGet {filename}".encode())
            while True:
                bytesRead = f.read(packetSize)
                if len(bytesRead) == 0:
                    break

                cliSock.sendall(bytesRead)

        print(f"{HOST}-{PORT}: {filename} has been sent successfully")
    except:
        print(f"{HOST}-{PORT}: Could not send {filename}")

    cliSock.close()


def receiveList():
    #sends list request to server
    cliSock.send(f"serverList".encode())

    #receive list string from server
    received = cliSock.recv(packetSize).decode()
    #seperate string into list
    fileList = received.split()

    print("Directory Files:")
    for i in fileList:
        print(i)

    cliSock.close()


#request table
if requestType == "get":
    download(str(sys.argv[4]))

elif requestType == "put":
    upload((sys.argv[4]))

elif requestType == "list":
    receiveList()

else:
    print("Error: Invalid Request Type")