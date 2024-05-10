import sys
from socket import socket, AF_INET, SOCK_DGRAM
from zlib import crc32
from struct import pack
rcvPort = int(sys.argv[1])
recv_addr = ('localhost', rcvPort)
rcvSocket = socket(AF_INET, SOCK_DGRAM)
rcvSocket.bind(recv_addr)
expected_seq_num = 0
while True:
    packet, send_addr = rcvSocket.recvfrom(64)
    transmittedMessage = packet[4:]
    checksum,sequence, content = packet[:4],packet[4:6],packet[6:]
    if (pack("I",crc32(transmittedMessage)) != checksum):
        rcvSocket.sendto(b'NAK',send_addr)
        continue
    if (expected_seq_num != int(sequence)):
        if (expected_seq_num == int(sequence) + 1):
            rcvSocket.sendto(b'ACK', send_addr)
            continue
        rcvSocket.sendto(b'ACK',send_addr)
        continue
    expected_seq_num = expected_seq_num + 1
    print(content.decode(),end="")
    rcvSocket.sendto(b'ACK',send_addr)
