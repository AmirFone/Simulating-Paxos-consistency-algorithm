# written by Amir
# Email:ahossain20@fordham.edu
# date: 11-30-2022
import socket
from time import sleep

def main():
    ip_port = ('127.0.0.1', 9992)
    s = socket.socket()
    s.connect(ip_port)
    while True:
        msg=s.recv(1024).decode()
        if msg=='Can Coordinator commit a value':
            temp="YES"
            s.sendall(temp.encode())
            msg=s.recv(1024).decode()
            f=open("participant_two.txt", "w")
            f.write(msg)
            f.close()
            temp="committed"
            s.sendall(temp.encode())
        else:
            print(msg)

    s.close()


if __name__ == "__main__":
    main()  