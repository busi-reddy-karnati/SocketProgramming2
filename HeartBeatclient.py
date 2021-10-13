import socket
import time
responses = []


def ping(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (host, port)
    sock.settimeout(1)
    try:
        for seq_num in range(1, 11):
            try:
                start_time = time.time()
                print(str(start_time)+"  starttime")
                message = 'Ping ' + str(seq_num) +" "+ str(start_time)
                send_message = sock.sendto(message.encode(), server_address)
                print("Sent " + message + " to Server")
                message_from_server, server = sock.recvfrom(4096)
                end_time = time.time()
                print("Received " + message_from_server.decode()+" from server")
                round_trip_time = end_time - start_time
                print("Round Trip Time: " + str(round_trip_time) + " seconds\n")
                responses.append((seq_num, message_from_server.decode(), round_trip_time))
            except socket.timeout:
                # print(str(seq_num) + " Requested Time out\n")
                responses.append((seq_num, "Request timed out", 0))

    finally:
        # print("closing socket")
        sock.close()
    return responses


if __name__ == "__main__":
    ping('localhost', 9023)
    print(responses)

