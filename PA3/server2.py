#!env python

"""Chat server for CST311 Programming Assignment 3"""
__author__ = "Team 8"
__credits__ = [
  "Michael Cervantes",
  "Jerry Do",
  "Ramo Tucakovic"
]

import socket as s
import time
import threading

# Configure logging
import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

server_port = 12000

serverMsg = "X: \"\", Y: \"\""
counter = 0
MAX = 2
clientList = []
#msgQueue = []
#lock = threading.Lock()

def debugPrt(msg):
    print("[[|||||| Thread:" + str(msg))

def connection_handler(connection_socket):
    global clientList
    global MAX
    #global msgQueue

    query = connection_socket.recv(1024)
    query_decoded = query.decode()
    log.info("Recieved query test \"" + str(query_decoded) + "\"")
    #time.sleep(5)
    # response = query_decoded.upper()
    # connection_socket.send(response.encode())
    # connection_socket.close()
    id = clientList.index(connection_socket)
    
    client = threading.Thread(target=msgThread, args=(query_decoded, id))
    #msgQueue.append(query_decoded)
    #print(str(threading.active_count()))
    client.start()

    time.sleep(1)

    client.join()

    # connection_socket.send(serverMsg.encode())
    # connection_socket.close()


def msgThread(msg, id):
    global serverMsg

    #lock = threading.Lock()

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
    global lock

    server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)

    server_socket.bind(('', server_port))

    server_socket.listen(MAX)

    log.info("The server is ready to reveive on port " + str(server_port))

    try:
        while True:
            connection_socket, address = server_socket.accept()
            log.info("connected to client at " + str(address))

            
            clientList.append(connection_socket)
            # for i in clientList:
            #     print("\n" + str(i) + "\n")

            if len(clientList) >= MAX:
                print("Two clients added?") #remove
                break

        for i in clientList:
            connection_handler(i)
        
        #close connections and send msg
        for i in clientList:
            i.send(serverMsg.encode())
            i.close()

    finally:
        print("Server closed")
        server_socket.close()

if __name__ == "__main__":
  main()