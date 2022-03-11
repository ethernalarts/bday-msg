
import socket

HOST = ("smtp-mail.outlook.com", 587)


def check_port(HOST):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((HOST, int(22)))
        s.shutdown(2)
        print("\nPort is open \n")
        return True
    except:
        print("\nPort is closed \n")
        return False


check_port(HOST)
