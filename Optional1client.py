import socket
import time

responses = []
max_min_avg_lossrate = []


def ping(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (host, port)
    sock.settimeout(1)
    min_round_trip_time = 1
    max_round_trip_time = 0
    total_round_trip_time = 0
    packets_lost = 0
    try:
        for seq_num in range(1, 11):
            try:
                start_time = time.time()
                message = 'Ping ' + str(seq_num) + " " + str(start_time)
                send_message = sock.sendto(message.encode(), server_address)
                print("Sent " + message + " to Server")
                message_from_server, server = sock.recvfrom(4096)
                end_time = time.time()
                print("Received " + message_from_server.decode() + " from server")
                round_trip_time = end_time - start_time
                max_round_trip_time = max(round_trip_time, max_round_trip_time)
                min_round_trip_time = min(round_trip_time, min_round_trip_time)
                total_round_trip_time = total_round_trip_time + round_trip_time
                print("Round Trip Time: " + str(round_trip_time) + " seconds\n")
                responses.append((seq_num, message_from_server.decode(), round_trip_time))
            except socket.timeout:
                print(str(seq_num) + " Request Timed out\n")
                packets_lost = packets_lost + 1
                responses.append((seq_num, "Request Timed Out", 0))

    finally:
        # print("closing socket")
        sock.close()
        if packets_lost != 10:
            avg_round_trip_time = total_round_trip_time / (10 - packets_lost)
        else:
            avg_round_trip_time = 0
        max_min_avg_lossrate.append(max_round_trip_time)
        max_min_avg_lossrate.append(min_round_trip_time)
        max_min_avg_lossrate.append(avg_round_trip_time)
        max_min_avg_lossrate.append(packets_lost * 10)


if __name__ == "__main__":
    ping('localhost', 9023)
    for response in responses:
        print(response)
    print('====================Statistics====================')
    print("Max Round Trip Time: " + str(max_min_avg_lossrate[0]))
    print("Min Round Trip Time: " + str(max_min_avg_lossrate[1]))
    print("Average round trip time : " + str(max_min_avg_lossrate[2]))
    print("Packet Loss Rate: " + str(max_min_avg_lossrate[3]) + " %")
