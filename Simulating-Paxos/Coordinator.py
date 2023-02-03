# written by Amir
# Email:ahossain20@fordham.edu
# date: 11-30-2022
from time import sleep
import socket
import threading
import sys
part_one=[]
part_two=[]
result_of_the_transaction=[]
all_lock=0
Clint=[]
vote=[]
def phase_one_and_two_logic_p1(conn):
    global all_lock
    if part_one:
        temp="Can Coordinator commit a value"
        conn.sendall(temp.encode())
        msg=conn.recv(1024).decode()
        if "YES" in msg:
            sleep(1)
            all_lock+=1
            temp=part_one[-1]
            conn.sendall(temp.encode())
            msg=conn.recv(1024).decode()
            if "committed" in msg:
                result_of_the_transaction.append('committed')
            else:
                result_of_the_transaction.append('Aborted')
        part_one.pop()
    return

def participant_one():
    global all_lock
    ip_port = ('127.0.0.1', 9991)
    sk = socket.socket()
    sk.bind(ip_port)
    print('connecting to participant_one')
    sk.listen(5) 
    conn, addr = sk.accept()
    print('connected to participant_one')
    while True:
        if part_one: phase_one_and_two_logic_p1(conn)
def phase_one_and_two_logic_p2(conn):
    global all_lock
    temp="Can Coordinator commit a value"
    conn.sendall(temp.encode())
    msg=conn.recv(1024).decode()
    if "YES" in msg:
        all_lock+=1
        # making sure we have all the need locks 
        count=0
        while all_lock<2:
            if count==5:
                result_of_the_transaction.append('Aborted')
                part_two.pop()
                part_one.pop()
                break
            sleep(2)
            print('waiting to acquire all locks')
            count+=1
        else:
            print('locks acquire!')
        temp=part_two[-1]
        conn.sendall(temp.encode())
        msg=conn.recv(1024).decode()
        if "committed" in msg:
            result_of_the_transaction.append('committed')
        else:
            result_of_the_transaction.append('Aborted')
    part_two.pop()
    return 

def participant_two():
    global all_lock
    ip_port = ('127.0.0.1', 9992)
    sk = socket.socket()
    sk.bind(ip_port)
    sk.listen(5)
    print('connecting to participant_two') 
    conn, addr = sk.accept()
    print('connected to participant_two') 
    while True:
        if part_two: phase_one_and_two_logic_p2(conn)

def preparing_transaction(msg):
    curr=msg.split(',')
    curr[0]=int(curr[0])
    curr[-1]=int(curr[-1])
    # Transfer 100 dollars from A to B
    curr[0]-=100
    curr[-1]+=100
    # adding bonus 20%
    curr[0]*=1.2
    curr[-1]+=curr[0]*.2
    part_one.append(str(curr[0]))
    part_two.append(str(curr[-1]))

def Client_msg():
    ip_port = ('127.0.0.1', 9993)
    sk = socket.socket()
    sk.bind(ip_port)
    sk.listen(5)
    print('connecting to Client')
    conn, addr = sk.accept()
    print('connected to Client')
    Clint.append(conn)
    while True:
        msg=conn.recv(1024).decode()
        preparing_transaction(msg)

def main():
    t = threading.Thread(target=participant_one,args=())
    t.start()
    t = threading.Thread(target=participant_two,args=())
    t.start()
    t = threading.Thread(target=Client_msg,args=())
    t.start()
    while True:
        if 'Aborted' in result_of_the_transaction:
            temp="transaction was aborted please try again"
            Clint[0].sendall(temp.encode())
            sys.exit(1)
        elif "committed" in result_of_the_transaction and len(result_of_the_transaction)==2:
            temp="Transaction Finished"
            Clint[0].sendall(temp.encode())
            sys.exit(1)

if __name__ == "__main__":
    main()