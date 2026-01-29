import socket, sys

file = 'rsdatabase.txt'
Lsfile = 'lsdatabase.txt'

data2 = open('lsdatabase.txt')
tld1 = data2.readline().lower().strip()
tld2 = data2.readline().lower().strip()
rs = data2.readline().lower().strip()
TS1 = data2.readline().lower().strip()
TS2 = data2.readline().lower().strip()
AS = data2.readline().lower().strip()
data2.close()


handlerDict = {}
def parseFile():
    data = open('rsdatabase.txt', 'r')
    for line in data:
        temp = line.lower().strip().split(' ') # I did lower so i would be case insensitive according to pdf
        handlerDict[temp[0]] = temp[1]
    data.close()

def search(domain):
    if domain in handlerDict:
        return handlerDict[domain]
    
    return "0.0.0.0"

#so the query will come here
#then we will parse the file
#we check the query domain ending to see if the tld might have, if we have, we send back a reply with 
#the tld info to ls. 
#if the ending doesn't exist in TLD, check in rsdatabase

def whichTsHas(name):
    getExtension = name.split('.')
    temp = getExtension[::-1]
    checker = temp[0]
    
    if(checker == tld1):
        return TS1
    elif(checker == tld2):
        return TS2
    else:
        return None #doesn't matter


def choice(NAME, text):
    Asdf = whichTsHas(name=NAME)
    if(Asdf == TS1):
        inputQuery = text.split(" ") #now we have a list with a split of the three things    
        reply = "1" + " " + inputQuery[1] + " " +  TS1+  " " + inputQuery[2] + " " + 'ns' + "\n"
    elif(Asdf == TS2):
        inputQuery = text.split(" ") #now we have a list with a split of the three things    
        reply = "1" + " " + inputQuery[1] + " " +  TS2 +  " " + inputQuery[2] + " " + 'ns' + "\n"
    else:
        reply = replyToSend(text=text)
    return reply





def replyToSend(text): 
    parseFile()
    inputQuery = text.split(" ") #now we have a list with a split of the three things    
    domainIP = search(inputQuery[1].lower())
    if(domainIP == "0.0.0.0"): flag = 'nx' 
    else: flag = 'aa'
    reply = "1" + " " + inputQuery[1] + " " +  domainIP +  " " + inputQuery[2] + " " + flag + "\n"
    #1 domain ip id 
    return reply

def rs(rudns_port):
    
    PORT = int(rudns_port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    s.bind(('', PORT))
    s.listen(5)
    print("[S] listening on", s.getsockname())
    while(True):
        conn, addr = s.accept()
        print("[S] accepted connection from", addr)
        print("[S] accepted connection from", addr)
        
        out = open("rsresponsest.txt", "a") #change
        while True:
            data = conn.recv(1024)

            if not data:
                break
            text_ = data.decode().strip().lower() #this was the data in the last file
            tempz = text_.split(" ")
            a = choice(tempz[1], text=text_)
            #x = replyToSend(text=text_)
            conn.sendall(a.encode('utf-8'))
            out.write(a)
        # TODO: send reply back to client (with newline)

    out.close()
    conn.close()
    # TODO: Write your code here


if __name__ == '__main__':
    args = sys.argv
    rs(args[1])