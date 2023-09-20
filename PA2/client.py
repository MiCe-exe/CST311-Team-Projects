#Server address and port
server_address = ('localhost', 12000)

#Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Number of pings to send
num_pings = 10

#Initialize variables for statistics
min_rtt = float('inf')
max_rtt = 0
total_rtt = 0
packets_lost = 0

#Set socket timeout (1 second)
client_socket.settimeout(1.0)

for ping_num in range(1, num_pings + 1):
    

    try:
        # Record the time the packet is sent
        start_time = time.time()
        
        # Create the message to send
        message = f"Ping {ping_num} {time.time()}"        
        
        #Send the ping request
        client_socket.sendto(message.encode(), server*address)
        
        #Receive the response
        response = client_socket.recvfrom(1024)

        ##error here
        #Calculate round-trip time (RTT)
        rtt = (time.time() - start_time) * 1000  # Convert to milliseconds
