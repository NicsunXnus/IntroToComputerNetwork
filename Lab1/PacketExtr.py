import sys
def extract_packets_simple():
    size = sys.stdin.buffer.read(6) #reads Size:_
    nextChar = sys.stdin.buffer.read1(1).decode()
    num = ''
    while nextChar != "B":
        num += nextChar
        nextChar = sys.stdin.buffer.read1(1).decode()
            
    packet = sys.stdin.buffer.read(int(num))
    sys . stdout . buffer . write ( packet )
    sys . stdout . buffer . flush ()

def test():
    size = sys.stdin.buffer.read(6)
    print(len(size) == 6)

def extract_packets():
    window = sys.stdin.buffer.read(6) #reads Size:_
    while len(window) == 6:
        nextChar = sys.stdin.buffer.read(1).decode()
        num = ''
        while nextChar != "B":
            num += nextChar
            nextChar = sys.stdin.buffer.read(1).decode()
                
        packet = sys.stdin.buffer.read(int(num))
        sys . stdout . buffer . write ( packet )
        sys . stdout . buffer . flush ()
        window = sys.stdin.buffer.read(6)

extract_packets()
#test()