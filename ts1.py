import socket, sys

#STRICTLY HANDLES ROOT SERVER
# TODO: Add any helper functions if you need
file = 'ts1database.txt'
handlerDict = {}
def parseFile():
    data = open('ts1database.txt', 'r')
    for line in data:
        temp = line.lower().strip().split(' ') # I did lower so i would be case insensitive according to pdf
        handlerDict[temp[0]] = temp[1]
    data.close()

    
def search(domain):
    if domain in handlerDict:
        return handlerDict[domain]
    
    return "0.0.0.0"

#STRICTLY HANDLES ROOT SERVER
#STRICTLY HANDLES ROOT SERVER

def replyToSend(text):
    parseFile()
    inputQuery = text.split(" ") #now we have a list with a split of the three things    
    domainIP = search(inputQuery[1].lower())
    if(domainIP == "0.0.0.0"): flag = 'nx' 
    else: flag = 'aa'
    reply = "1" + " " + inputQuery[1] + " " +  domainIP +  " " + inputQuery[2] + " " + flag + "\n"
    #1 domain ip id 
    return reply

def ts1(rudns_port):
   
    PORT = int(rudns_port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    s.bind(('', PORT))
    s.listen(5)
    print("[S] listening on", s.getsockname())
    while(True):
        conn, addr = s.accept()
        print("[S] accepted connection from", addr)
        
        out = open("ts1responses.txt", "a") #change
        while True:
            data = conn.recv(1024)
            if not data:
                break
            text_ = data.decode().strip() #this was the data in the last file
            x = replyToSend(text=text_)
            conn.sendall(x.encode('utf-8'))
            out.write(x)

    out.close()
    conn.close()

if __name__ == '__main__':
    args = sys.argv
    ts1(args[1]) #this is the port number

