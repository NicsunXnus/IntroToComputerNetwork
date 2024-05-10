import zlib
import sys

def calculate_checksum(file_name):
    with open(file_name, 'rb') as file:
        contents = file.read()
        checksum = zlib.crc32(contents)
        print(checksum)

# Get the file name from the command-line argument
if len(sys.argv) > 1:
    file_name = sys.argv[1]
    calculate_checksum(file_name)