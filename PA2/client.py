import socket
import time

#Server address and port
server_address = '10.0.0.1'
server_port = 12000

#Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Number of pings to send
num_pings = 10

#Initialize variables for statistics
min_rtt = 1000.0
max_rtt = 0.0
tot_rtt = 0.0
avg_rtt = 0.0
packets_lost = 0

ALPH = .125
BETA = .25
rtt_est = 0.0
rtt_dev = 0.0

#Set socket timeout (1 second)
client_socket.settimeout(1.0)

for ping in range(1, num_pings + 1):
    # Record the time the packet is sent
    start_time = time.time()
        
    # Create the ping message
    message = f"Ping {ping}: "    
    try:
        #Send the ping request
        client_socket.sendto(message.encode(), (server_address, server_port))
        
        #Receive the response
        response, _ = client_socket.recvfrom(1024)
            
        #Calculate round-trip time (RTT), convert to ms
        #rtt = 0.0
        rtt = (time.time() - start_time) * 1000

        #Recalculate min, max, and total rtt
        tot_rtt += rtt
        if(rtt<min_rtt):
            min_rtt = rtt
        if(rtt>max_rtt):
            max_rtt = rtt

        #Setting ping 1's estimated and deviation RTT
        #Also setting min and max rtt
        if(ping==1):
            rtt_est, rtt_dev, min_rtt, max_rtt = rtt, rtt/2, rtt, rtt #/1.5 = clsoer results
            #rtt_dev = rtt_est / 2
        else:
            #Calculate estimated RTT
            rtt_est = ((1-ALPH)*rtt_est)+(ALPH*rtt)
        
            #Calculate deviation RTT
            rtt_dev = ((1-BETA)*rtt_dev)+(BETA*abs(rtt-rtt_est))

        print(message + "sample rtt = %.3f"%rtt 
              + " ms, estimated_rtt = %.3f"%rtt_est 
              + " ms, dev_rtt = %.3f"%rtt_dev)
    except socket.timeout:
        #if no reply within 1 second
        print(message + "Request timed out")
        packets_lost+=1
    if(ping==10):
        #print statistics
        print("Summary values:")
        print("min_rtt  = %.3f"%min_rtt + " ms")
        print("max_rtt  = %.3f"%max_rtt + " ms")
        print("avg_rtt = %.3f"%(tot_rtt/num_pings) + " ms")
        print("Packet loss: %.2f"%((packets_lost/num_pings)*100) + "%")
        print("Timeout Interval: %.3f"%(rtt_est+(4*rtt_dev)) + " ms")
client_socket.close()
