# !/usr/bin/env python3
import os
import sys
from Cryptodome.Hash import SHA256

if len(sys.argv) < 3:
    print("Usage: python3 ", os.path.basename(__file__), "key_file_name document_file_name")
    sys.exit()

key_file_name   = sys.argv[1]
file_name       = sys.argv[2]

# get the authentication key from the file
# TODO
with open(key_file_name, 'rb') as f:
    key = f.read()
# read the input file
with open(file_name, 'rb') as f:
    data = f.read()
# First 32 bytes is the message authentication code
# TODO
mac_from_file = data[:32] #H(m + s)
# Use the remaining file content to generate the message authentication code
# TODO
h = SHA256.new(data[32:]) #H(m)
h.update(key) #H(m + s)
mac_generated = h.digest()
if mac_from_file == mac_generated:
    print ('yes')
else:
    print ('no')
