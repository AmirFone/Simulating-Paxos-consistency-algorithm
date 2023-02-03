# written by Amir
# Email:ahossain20@fordham.edu
# date: 11-30-2022
import socket
def main():
    ip_port = ('127.0.0.1', 9993)
    s = socket.socket()
    s.connect(ip_port)
    while True:
        inp = input('input value to be porposed(ex[A:100,B:200]):').strip()
        if not inp:
            continue
        # sending proposed value to node two
        s.sendall(inp.encode())
        print("sent to Coordinator",inp)
        msg=s.recv(1024).decode()
        print("Final State: ",msg)

if __name__ == "__main__":
    main()