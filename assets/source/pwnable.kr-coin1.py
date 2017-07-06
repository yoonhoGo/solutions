import socket
import re
import time

rule = re.compile("N=(?P<number>\d+) C=(?P<count>\d+)")

def netcat(hostname, port, content):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostname, port))
    # recv intro and print
    str_intro = s.recv(2048).decode()
    print(str_intro)
    time.sleep(3)
    for i in range(100):
        #  recv rule, parse and print
        str_NnC = s.recv(20).decode()
        # print(str_NnC)
        result = rule.match(str_NnC)
        number = int(result.group("number"))
        count = int(result.group("count"))
        # print(number, count)
        result = [str(x) for x in range(number)]
        while True:
            # send string
            # print('**__%d__**' %(count))
            if len(result) == 1:
                # print('['+result[0]+']')
                s.sendall((str(result[0])+"\n\r").encode())
            else:
                # print('['+' '.join(result[:int(len(result)/2)]), end='] / ')
                # print(' '.join(result[int(len(result)/2):]))
                s.sendall((' '.join(result[:int(len(result)/2)]) + "\n\r").encode())
            # recv data
            while True:
                data = s.recv(30).decode()
                # print("Received:", data)
                if data :
                    break
                # print("wait.", end=" ")
            count-=1
            if "Correct!" in data:
                break
            elif data[-2] == '9':
                if len(data) < 3:
                    for i in range(count+1):
                        s.sendall((str(result[0])+"\n\r").encode())
                        while True:
                            data = s.recv(1024).decode()
                            if data :
                                print("Received:", data)
                                break
                    break
                result = result[:int(len(result)/2)] if len(result) != 1 else [result[0]]
            else:
                result = result[int(len(result)/2):] if len(result) != 1 else [result[0]]
    while True:
        data = s.recv(1024).decode()
        if data :
            print("Received:", data)
            break
    print("Connection closed.")
    s.close()

netcat("pwnable.kr", 9007, "")
