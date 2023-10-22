#!env python

"""Chat server for CST311 Programming Assignment 3"""
__author__ = "Team 8"
__credits__ = [
  "Michael Cervantes",
  "Jerry Do",
  "Ramo Tucakovic"
]

# Mulit threading is needed to stop the program from proccessing the first instructions
# before the second one is process. This cuases a rat race. Threading adds a layer of 
# synchronize. Both clients can get both inputs from eacher.

import socket as s
import time
import threading

# Configure logging
import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

server_port = 12000

#global variables each client might interact with
serverMsg = "X: \"\", Y: \"\""
counter = 0
MAX = 2
clientList = []
#msgQueue = []
threadQueue = []

lock = threading.Lock()
counter = 0

# connection handler for each client that is created.
# from here we can use multi Threading to access the messaging queue
def connection_handler(connection_socket):
    global clientList
    global MAX
    global lock

    lock.acquire()
    query = connection_socket.recv(1024)
    lock.release()
    query_decoded = query.decode()
    log.info("Recieved query test \"" + str(query_decoded) + "\"")

    # Get client ID, Client X = 0, client Y = 1
    id = clientList.index(connection_socket)
    
    msgThread(query_decoded, id)

def msgThread(msg, id):
    global serverMsg
    global lock

    # message from both clients merged.
    #lock.acquire()
    if id == 0:
        serverMsg = serverMsg[:4] + msg + serverMsg[4:]
        time.sleep(10)
    elif id == 1:
        serverMsg = serverMsg[:(len(serverMsg)-1)] + msg + serverMsg[(len(serverMsg)-1):]
    else:
        serverMsg = serverMsg + ", " + str(id) + ":{}".format(msg)
    #lock.release()

def main():
    global clientList
    #global lock
    global threadQueue

    server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)

    server_socket.bind(('', server_port))

    server_socket.listen(MAX)

    log.info("The server is ready to reveive on port " + str(server_port))

    try:
        while True:
            connection_socket, address = server_socket.accept()
            log.info("connected to client at " + str(address))
            clientList.append(connection_socket)

            if len(clientList) >= MAX:
                break

        for i in clientList:
            #connection_handler(i)
            threadQueue.append(threading.Thread(target=connection_handler(i)))

        for i in threadQueue:
            i.start()
            time.sleep(1)
            i.join()

        #close connections and send msg
        for i in clientList:
            i.send(serverMsg.encode())
            i.close()

    finally:
        print("Server closed")
        server_socket.close()

if __name__ == "__main__":
  main()