import sys
from socket import socket, AF_INET, SOCK_DGRAM, timeout as TimeoutException
from zlib import crc32
from struct import pack
# Format of packet: checksum (4B) |sequence_num (2B) |data (58B)
def read_from_stdin():
     num_bytes = 58
     data = bytearray()
     while num_bytes > 0:
        msg = sys.stdin.buffer.read1(num_bytes)
        if len(msg) == 0:
            break
        data.extend(msg)
        num_bytes -= len(msg)
     return data

unreliNetPort = int(sys.argv[1])
send_addr = ('localhost',unreliNetPort)
currIndex = 0
sendSocket = socket(AF_INET, SOCK_DGRAM)
sendSocket.settimeout(0.050)
data = read_from_stdin()
while (True):
    if len(data) == 0:
        break
    transmittedMessage = '{:02d}'.format(currIndex).encode() + data
    checksum = pack("I",crc32(transmittedMessage))
    packet = checksum + transmittedMessage
    while (True):
        try:
            sendSocket.sendto(packet,send_addr)
            response,_ = sendSocket.recvfrom(64)
            if (response != b'ACK'):
                continue
            break
        except TimeoutException:
            continue
    currIndex = currIndex + 1
    data = read_from_stdin()
sendSocket.close()
