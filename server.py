import os
import sys
import socket

#initialise host and port
HOST = "0.0.0.0"
PORT = int(sys.argv[1])

packetSize = 4096

#create server socket and bind server to port
srvSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srvSock.bind((HOST, PORT))

print(f"Server up and running on {PORT} with address {HOST}")

#can listen for up to 5 connections to its socket
srvSock.listen(5)

def download(request):

    filename = request
    #change filename to write into server to basename
    readInFile = os.path.basename(filename)

    #check for identical filename, disallow overwrite
    if readInFile in os.listdir():
        print(f"{HOST}-{PORT}: Cannot overwrite existing file.")
    else:
        try:
            #procedure to write file into server folder
            with open(readInFile, "wb") as f:
                while True:
                    bytesRead = clientSocket.recv(packetSize)
                    if len(bytesRead) == 0:
                        break

                    f.write(bytesRead)


            print(f"{HOST}-{PORT}: {filename} received from {address[0]}")
        except:
            #print error message if problem occurs
            print(f"{HOST}-{PORT}: Could not receive file from {address[0]}")


def upload(request):

    filename = request
    try:

        with open(filename, "rb") as f:
            clientSocket.send(f"{filename}".encode())
            while True:
                bytesRead = f.read(packetSize)
                if len(bytesRead) == 0:
                    break
                            
                clientSocket.sendall(bytesRead)
            print(f"{HOST}-{PORT}: {filename} sent successfully to {address[0]}")
    except:
        print(f"{HOST}-{PORT}: There was a problem sending file {filename} to {address[0]}")



def sendList():
    files = os.listdir()

    #deletes itself from list of files
    files.remove("server.py")

    #joins list to send data across as string
    files = f" ".join(files)

    clientSocket.send(f"{files}".encode())
    print(f"{HOST}-{PORT}: List sent successfully")


#loop keeps server open until someon manually closes it
while True:

    #accept connection from incoming client and print client address
    clientSocket, address = srvSock.accept()
    print(f"{address[0]}: Connected.")

    try:
        #receives request from client
        received = clientSocket.recv(packetSize).decode()
        request = received.split()
        requestType = request[0]

        #request table, runs method corresponding to method called in client
        if requestType == "serverGet":
            download(request[1])

        elif requestType == "serverPut":
            upload(request[1])

        elif requestType == "serverList":
            sendList()

    except:
        print(f"{HOST}-{PORT}: Error receiving request from {address[0]}")

    clientSocket.close()

#close the server socket
srvSock.close()

exit(0)
