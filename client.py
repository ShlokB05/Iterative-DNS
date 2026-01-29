import socket, sys
CurrReqNum = 1
# TODO: Add any helper functions if you need
def toSend(domain):
    global CurrReqNum
    req = "0" + " " + domain + " " + str(CurrReqNum) + '\n'
    CurrReqNum = CurrReqNum + 1
    return req

def client(ls_hostname, rudns_port):
    # Read database
    with open('hostnames.txt', 'r') as fd:
        requests = list(map(lambda l: l.strip().lower(), fd.readlines()))
        output = open("resolved.txt", 'a')
    
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect((ls_hostname, int(rudns_port)))
    for i in range(0, len(requests)):
        x = toSend(requests[i])
        c.sendall(x.encode('utf-8'))
        reply = (c.recv(1024)).decode('utf-8')
        output.write(reply)


    output.close()
    c.close()
    print("It works ")


if __name__ == '__main__':
    args = sys.argv
    client(args[1], args[2])
