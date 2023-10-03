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

def connection_handler(connection_socket, address):
  # Read data from the new connectio socket
  #  Note: if no data has been sent this blocks until there is data
  query = connection_socket.recv(1024)

  # Decode data from UTF-8 bytestream
  query_decoded = query.decode()
  
  # Log query information
  log.info("Recieved query test \"" + str(query_decoded) + "\"")

  # Perform some server operations on data to generate response
  time.sleep(10)
  response = query_decoded.upper()   #In this case we dont have to convert to upper

  # Sent response over the network, encoding to UTF-8
  connection_socket.send(response.encode())
  
  # Close client socket
  connection_socket.close()

def cThread(connection_socket, address, userID):
  lock = threading.Lock()
  global serverMsg

  query = connection_socket.recv(1024)
  query_decoded = query.decode()
  
  # Log query information
  log.info("Recieved query test \"" + str(query_decoded) + "\"")

  with lock:
    if userID == 1:
      serverMsg = serverMsg[:4] + query_decoded + serverMsg[4:]
    elif userID == 2:
      serverMsg = serverMsg[:(len(serverMsg)-1)] + query_decoded + serverMsg[(len(serverMsg)-1):]
    else:
      serverMsg = serverMsg + ", " + str(userID) + ":{}".format(query_decoded)
    
  
  #time.sleep(10)
  connection_socket.send(serverMsg.encode())
  global counter
  counter -= 1

  #connection_socket.close()
  

def main():
  # Create a TCP socket
  # Notice the use of SOCK_STREAM for TCP packets
  server_socket = s.socket(s.AF_INET,s.SOCK_STREAM)
  
  # Assign IP address and port number to socket, and bind to chosen port
  server_socket.bind(('',server_port))
  
  # Configure how many requests can be queued on the server at once
  server_socket.listen(MAX)
  
  # Alert user we are now online
  log.info("The server is ready to receive on port " + str(server_port))
  
  # Surround with a try-finally to ensure we clean up the socket after we're done
  try:
    # Enter forever loop to listen for requests
    while True:
      # When a client connects, create a new socket and record their address
      connection_socket, address = server_socket.accept()
      log.info("Connected to client at " + str(address))

      global counter
      counter += 1
      
      clientThreadX = threading.Thread(target=cThread, args=(connection_socket, address, counter))
      clientThreadY = threading.Thread(target=cThread, args=(connection_socket, address, counter))

      clientThreadY.start()
      clientThreadX.start()

      #time.sleep(2)

      clientThreadX.join()
      clientThreadY.join()
      

  finally:
    print("++++++++++EXIT+++++++++++++")
    server_socket.close()


if __name__ == "__main__":
  main()
