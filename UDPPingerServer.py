import random
import socket
from socket import *
import time
import hashlib
import sys


def serve(port):
    server_socket = socket(AF_INET, SOCK_DGRAM)
    server_socket.bind(('127.0.0.1', port))
    while True:
        try:
            random_number = random.randint(0, 10)
            message, address = server_socket.recvfrom(1024)
            if random_number < 4:
                continue
            split_message = message.decode().split()
            seq_num = split_message[1]
            client_time = split_message[5]
            server_time = time.time()
            hash_digest = hashlib.md5('seq:{0},c_time:{1},s_time:{2},key:{3}'.format(seq_num,
                                                                                     client_time,
                                                                                     str(server_time),
                                                                                     'randomkey').encode()).hexdigest()
            print(split_message)
            response = 'Reply {0} {1} {2} {3}\n'.format(seq_num, client_time, str(server_time), hash_digest)
            server_socket.sendto(response.encode(), address)
        except KeyboardInterrupt:
            server_socket.close()
            sys.exit()
        except:
            continue


if __name__ == "__main__":
    serve(9023)
