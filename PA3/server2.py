#!env python

"""Chat server for CST311 Programming Assignment 3"""
__author__ = "[team name here]"
__credits__ = [
  "Your",
  "Names",
  "Here"
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
#lock = threading.Lock()

def debugPrt(msg):
    print("[[|||||| Thread:" + str(msg))

def connection_handler(connection_socket):
    # Old code
    global clientList

    query = connection_socket.recv(1024)
    query_decoded = query.decode()
    log.info("Recieved query test \"" + str(query_decoded) + "\"")
    #time.sleep(5)
    # response = query_decoded.upper()
    # connection_socket.send(response.encode())
    # connection_socket.close()
    id = clientList.index(connection_socket)
    
    client = threading.Thread(target=msgThread, args=(query_decoded, id))
    
    client.start()

    #time.sleep(1)

    client.join()

    connection_socket.send(serverMsg.encode())
    connection_socket.close()

    # while True:
    #     if t.active_count() >= MAX:
    #         t.Thread.join()

def msgThread(msg, id):
    global serverMsg

    if id == 0:
        serverMsg = serverMsg[:4] + msg + serverMsg[4:]
        #time.sleep(10)
    elif id == 1:
        serverMsg = serverMsg[:(len(serverMsg)-1)] + msg + serverMsg[(len(serverMsg)-1):]
    else:
        serverMsg = serverMsg + ", " + str(id) + ":{}".format(msg)

def main():
    global clientList
    #global lock

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

    finally:
        server_socket.close()

if __name__ == "__main__":
  main()