import socket
import os
import sys
import math

def responseHandler(client_socket, binRequest):
    request = str(binRequest)[2:-1]

    #handle interminttent requests
    while request.find("  ") == -1:
        #if it is GET,DELETE method, this will ensure a full
        #request. If it is POST method, this will ensure a full
        #header body
        binRequest = binRequest + client_socket.recv(1024)
        request = str(binRequest)
    
    request = str(binRequest)[2:-1]
    index = request.index("  ")
    front, contentBody =request[:index],request[index + 2:]
    method = request.split(' ')[0].upper()
    if (method.startswith('GET') or method.startswith('DELETE')):
        strArray = front.split(' ')
        method, header = strArray[0], strArray[1]
                    
        if header.startswith('/key/'):
            #HANDLE KEY EVENT
            key = header.split('/key/')[1]
            if method == 'GET':
                if key in key_value_store:
                    if key in counter_store: #if key has a retrieval time
                        response = ("200 OK Content-Length " + key_value_store[key][0] + "  ").encode() + key_value_store[key][1]
                        counter_store[key] = counter_store[key] - 1
                        if counter_store[key] == 0: #remove items when retrieval times falls to 0
                            counter_store.pop(key)
                            key_value_store.pop(key)
                    else:#if key has no retrieval time
                        response = ("200 OK Content-Length " + key_value_store[key][0] + "  ").encode() + key_value_store[key][1]
                else:
                    response = ("404 NotFound  ").encode()
                
            else:
                if key not in key_value_store:
                    response = ("404 NotFound  ").encode()
                else:
                    if key in counter_store:
                        response = ("405 MethodNotAllowed  ").encode()
                    else:
                        deletedContent = key_value_store.pop(key)
                        length, content = deletedContent[0], deletedContent[1]
                        response = ("200 OK Content-Length " + length + "  ").encode() + content
        elif header.startswith('/counter/'): #asks for counter
            #HANDLE COUNTER EVENT
            key = header.split('/counter/')[1]
            if method == 'GET': #HANDLE GET METHOD
                if key not in key_value_store:
                    response = ("404 NotFound  ").encode()
                else:
                    if key in counter_store:
                        response = ("200 OK Content-Length 1  " + str(counter_store[key])).encode()
                    else:
                        response = "200 OK Content-Length 8  Infinity".encode()
            else:
                if key not in counter_store:
                    response = "404 NotFound  ".encode()
                else:
                    retrievalTimes = str(counter_store.pop(key))
                    response = ("200 OK Content-Length 1  " + retrievalTimes).encode()
        # Send the response back to the client
        encodedResponse = response
        client_socket.send(encodedResponse)
        if contentBody != "": #persistent request
            binValue = binRequest[index + 2:]
            responseHandler(client_socket, binValue)
            
    elif (method.startswith('POST')):
        methodIndWsp = front.index(' ')
        keyPathIndWsp = front.index(' ', methodIndWsp + 1)
        keyHeader = front[methodIndWsp + 1: keyPathIndWsp]
    
        headers = front[keyPathIndWsp + 1:].lower()
        startOfLenHdr = headers.find("content-length") + 15
        length = 0
        lengthFinder = headers[startOfLenHdr:]
        if lengthFinder.find(' ') != -1:
            while True:
                while lengthFinder[length] != ' ':
                    length = length + 1
                try:
                    checkNum = int(lengthFinder[:length])
                    length = str(checkNum)
                    break
                except:
                    startOfLenHdr = lengthFinder.find("content-length") + 15
                    lengthFinder = lengthFinder[startOfLenHdr:]
                    length = 0
                    continue
        else:
            length = lengthFinder
        binValue = binRequest[index + 2:]
        binRequest = b''
        binValueLen = len(binValue)
        if (binValueLen > int(length)):
            binRequest = binValue[int(length):]
            binValue = binValue[:int(length)]
        elif (binValueLen < int(length)):
            while (len(binValue) < int(length)):
                binValue = binValue + client_socket.recv(1024)
        if len(binValue) > int(length):
            binRequest = binValue[int(length):]
            binValue = binValue[:int(length)]
        if keyHeader.startswith('/key/'):
            #HANDLE KEY EVENT
            key = keyHeader.split('/key/')[1]
            if key in counter_store:
                response = "405 MethodNotAllowed  "
            else:
                key_value_store[key] = (length, binValue)
                response = "200 OK  " 

        elif keyHeader.startswith('/counter/'): #asks for counter
            #HANDLE COUNTER EVENT
            key = keyHeader.split('/counter/')[1]
            if key not in key_value_store:
                response = "405 MethodNotAllowed  "
            else:
                if key not in counter_store:
                    counter_store[key] = int(binValue)
                else:
                    counter_store[key] = counter_store[key] + int(binValue)
                response = "200 OK  "
        
        encodedResponse = response.encode()
        client_socket.send(encodedResponse)
        if binRequest != b'':#persistent request
            responseHandler(client_socket, binRequest)


# Define the key-value store and counter store
key_value_store = {}
counter_store = {}
response = ""
# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a port number passed as a command-line argument
port = int(sys.argv[1])
server_socket.bind(('localhost', port))

# Listen to the socket and accept a new connection
server_socket.listen()
print('Listening on port', port)

while True:
    # Accept a new connection
    client_socket, client_address = server_socket.accept()
    print('Accepted connection from', client_address)
    while True:
        # Parse the client request
        request = client_socket.recv(32704)
        if not request:
            break
        responseHandler(client_socket,request)
    # Close the connection
    client_socket.close()
