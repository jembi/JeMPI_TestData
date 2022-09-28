import socket
import datetime

def create_file():
    f = open("output_log_file.txt", "w")
    f.write(str(datetime.datetime.now()) + "\n")
    f.write(str(socket.gethostname()) + "\n")
    f.write(str(socket.gethostbyname(socket.gethostname())) + "\n\n")


    f.close()
