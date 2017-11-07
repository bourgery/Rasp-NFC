import time
from bluetooth import *
import RPi.GPIO as GP


pin = 2
GP.setmode(GP.BCM)
GP.setup(pin,GP.OUT)
GP.setwarnings(False)




server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "00000000-0000-1000-8000-00805F9B34FB"
uuid = "11111111-1111-1111-1111-111111111111"

#advertise_service( server_sock, "AquaPiServer",
#                   service_id = uuid,
#                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
#                   profiles = [ SERIAL_PORT_PROFILE ]
#                   protocols = [ OBEX_UUID ]
#)





while True:
    try:
        print "Waiting for connection on RFCOMM channel %d" % port
        client_sock, client_info = server_sock.accept()
        print "Accepted connection from ", client_info
        while True:
	    try:
	            data = client_sock.recv(1024)
        	    if len(data) == 0: break
	            print "received [%s]" % data
                    if data == "on":
                        GP.output(pin,0)
                        data = "and I turn " + data + " the light"
                    elif data == "off":
                        GP.output(pin,1)
                        data = "and I turn " + data + " the ligth"
                    elif data == "change":
                        GP.output(pin,GP.input(pin) ^ 1)
                        data = "and I change the state of the ligth"
                    elif data == "close":
                        GP.output(pin,1)
	    	        client_sock.close()
    		    #server_sock.close()
    	                print "all done"
                        break
                    else:
                        data = "but no valid command found"
                    data = "I receive your data " + data
         	    client_sock.send(data)
		    print "sending [%s]" % data
    
            except IOError:
	        pass
        
	    except KeyboardInterrupt:
	        print "disconnected"
                GP.output(pin,1)
	        client_sock.close()
	        print "all done"

	        break

                
    except KeyboardInterrupt:
            server_sock.close()
            print("server socket close")
            break
