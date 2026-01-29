import socket, sys

# TODO: Add any helper functions if you need
file = 'lsdatabase.txt'


data2 = open('lsdatabase.txt')
tld1 = data2.readline().lower().strip()
tld2 = data2.readline().lower().strip()
rs = data2.readline().lower().strip()
TS1 = data2.readline().lower().strip()
TS2 = data2.readline().lower().strip()
AS = data2.readline().lower().strip()
data2.close()

handlerDict = {}

def search(domain):
    if domain in handlerDict:
        return handlerDict[domain]
    
    return None #go to root

def add(key,value):
    handlerDict[key] = value

#reply.decode('utf-8')
currid = 1




def MakingQuery(host, port,ogQuery):
    global currid
    reply = "0" + " " + ogQuery + " " + str(currid) + '\n'
    currid = currid + 1
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.sendall((reply.encode('utf-8')))
    reply2 = s.recv(1024).decode('utf-8').strip()
    s.close()
    return reply2


 
def replyToclientfromLS(text): 
    inputQuery = text.split(" ") #now we have a list with a split of the three things    
    domainIP = search(inputQuery[1].lower())
    if(domainIP): #we send the request
        flag = 'aa'
        reply = "1" + " " + inputQuery[1] + " " +  domainIP +  " " + inputQuery[2] + " " + flag + "\n"
    #1 domain ip id 
    return reply


def forwardReplyFromTS(text, clID):
    inputQuery = text.split(" ") #now we have a list with a split of the three things 
    if(inputQuery[4] == 'aa'):
        add(inputQuery[1].lower(), inputQuery[2])
    reply = "1" + " " + inputQuery[1] + " " +  inputQuery[2] +  " " + str(clID) + " " + inputQuery[4] + "\n"
    return reply

def ls(rudns_port):
   
    PORT = int(rudns_port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    s.bind(('', PORT))
    s.listen(5)
    print("[S] listening on", s.getsockname())
    conn, addr = s.accept()
    print("[S] accepted connection from", addr)
    
    out = open("lsresponses.txt", "a") #change
    while True:
        data = conn.recv(1024)
        if not data:
            break
        text_ = data.decode().strip() #this was the data in the last file
        temp = text_.split(' ') #this is still the query from client
        clientID = temp[2]
        if(search(temp[1].lower()) != None):
            FinalReply = replyToclientfromLS(text_)
        else:
            rootReply = MakingQuery(rs, PORT, temp[1])
            repl = rootReply.strip().split(" ")
            if(repl[4] == "ns"):
                newq = MakingQuery(repl[2], PORT, repl[1]) #now we go to the ts
                FinalReply = forwardReplyFromTS(newq, clID=clientID)
            elif(repl[4] == 'aa'): #if rs has
                FinalReply = forwardReplyFromTS(rootReply,clientID)
            else: #nx
                newq = MakingQuery(AS, PORT, temp[1]) #now we go to the ts
                FinalReply = forwardReplyFromTS(newq, clID=clientID)

            conn.sendall(FinalReply.encode('utf-8'))
            out.write(FinalReply)
    # TODO: send reply back to client (with newline)

    out.close()
    conn.close()
    s.close()
  

if __name__ == '__main__':
    args = sys.argv
    ls(args[1])


'''


def ts1(rudns_port):
    PORT = int(rudns_port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    s.bind(('', PORT))
    s.listen(1)
    print("[S] listening on", s.getsockname())
    conn, addr = s.accept()
    print("[S] accepted connection from", addr)
    out = open("out-ts1.txt", "w") #change
    while True:
        data = conn.recv(1024)
        if not data:
            break
        text_ = data.decode().strip() #this was the data in the last file
        x = replyToSend(text=text_)
        conn.sendall(x.encode('utf-8'))
        out.write(x)
    # TODO: send reply back to client (with newline)

    out.close()
    conn.close()
    s.close()
    # TODO: Write your code here

if __name__ == '__main__':
    args = sys.argv
    ts1(args[1]) #this is the port number





'''