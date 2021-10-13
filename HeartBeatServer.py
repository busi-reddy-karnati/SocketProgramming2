import socket
from socket import *
import time
import hashlib
import sys


def serve(port):
    server_socket = socket(AF_INET, SOCK_DGRAM)
    server_socket.bind(('127.0.0.1', port))
    latest_message_sequence = -1
    server_socket.settimeout(5)
    print("Heart Beat Server Up")
    while True:
        try:
            message, address = server_socket.recvfrom(1024)
            split_message = message.decode().split()
            seq_num = split_message[1]
            if seq_num - latest_message_sequence > 1:
                print("{} number of messages missing".format(seq_num-latest_message_sequence-1))
            else:
                print("Received Message of Sequence Number: {}".format(seq_num))
            latest_message_sequence = seq_num
            client_time = split_message[2]
            server_time = time.time()
            hash_digest = hashlib.md5('seq:{0},c_time:{1},s_time:{2},key:{3}'.format(seq_num,
                                                                                     client_time,
                                                                                     str(server_time),
                                                                                     'randomkey').encode()).hexdigest()
            response = 'Reply {0} {1} {2} {3}\n'.format(seq_num, client_time, str(server_time), hash_digest)
            server_socket.sendto(response.encode(), address)
        except Exception as e:
            if str(e) == "timed out":
                print("The Client Application is Down")
                server_socket.close()
                sys.exit()


if __name__ == "__main__":
    serve(9023)
