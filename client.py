import socket, fcntl, struct, sys, asyncoro, os, ntplib

class FileSplitterException(Exception):
    def __init__(self, value):
        self.value = value
 
    def __str__(self):
        return str(self.value)
def currenttime():
    c = ntplib.NTPClient()
    response = c.request('pool.ntp.org')
    return response.tx_time 
def get_ip_address(ifname):
    ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
    ip.fileno(),0x8915, # SIOCGIFADDR
    struct.pack('256s', ifname[:15]))[20:24])
t1 = currenttime()
print t1  
ip1 = get_ip_address('usb0')
ip2 = get_ip_address('eth1')
ip3 = get_ip_address('usb1')
print ip1, ip2, ip3

port = 44000
filename = '100MB.zip'
chunksize = 100000
numconn = 15
numpaths = 3
datalist = []
div1 = []
div2 = [None]* numconn
div3 = []
ratio = [1,2,1]
paths = []
print filename 

def split(filename,chunksize):
        global filesize
        global numchunks
        global numconn 
        try:
            f = open(filename, 'rb')
               
        except (OSError, IOError), e:
            raise FileSplitterException, str(e)
 
        filesize = os.path.getsize(filename)
        numchunks = int(filesize/chunksize)
        print numchunks
        chunksz = chunksize
        total_bytes = 0
 
        for x in range(numchunks):
            if x == numchunks - 1:
                chunksz = filesize - total_bytes
                
            try:
                data = f.read(chunksz)
                total_bytes += len(data)
                datalist.append(data)
            
            except (OSError, IOError), e:
                print e
                continue
             
        print 'Done.'

def client(host, port, sock, coro=None):
    global filename
    global numchunks
    global numconn     
    x = sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    sock = asyncoro.AsyncSocket(sock)
    try:
        yield sock.bind((host, port))
    except socket.error as err:
        print 'Bind Failed. Error: ' + str(err[0]) + 'Message' + err[1]
        sys.exit()
    host1 = '194.47.150.244'
    port3 = 8012
    
    yield sock.connect((host1, port3))
    for n in xrange(div3[x], div3[x+1]):
            msg = '%d:data' % (n) + str(numchunks) + ':data' + filename + ' ' + datalist[n]
            yield sock.send_msg(msg)
    #print "DAta sent through ", x
    yield sock.send_msg('terminate')  
                 
                    
            
    sock.close()
split(filename,chunksize)

div = numchunks/float(sum(ratio))
for n in xrange(0,len(ratio)):
    div1.append(int(round(div*ratio[n],0)))
divsum1 = sum(div1)
if divsum1 != numchunks:
    if divsum1 < numchunks:
        div1[-1] = div1[-1] + (numchunks-divsum1)
    else:
        div1[-1] = div1[-1] - (divsum1-numchunks)
print div1
no1 = int(numconn/numpaths)
no2 = numconn%numpaths
paths = [no1]*numpaths

if no2 != 0:
    
    for n in xrange (0, no2):
        
        paths[n] = paths[n] + 1
print paths 
        
for i in xrange (0, numpaths):
    counter = 0
    j = 0     
    for n in xrange (0, numconn):
        
        if n%numpaths == 0:
            if n+i < numconn:
                                
                div2[n+i] = int(round(div1[i]/paths[i],0))
                counter += div2[n+i]
                j = n 
    print counter,j   
            
    if counter != div1[i]:
        if counter < div1[i]:
            div2[j] = div2[j] + (div1[i]-counter)
        else:
            div2[j] = div2[j] - (counter-div1[i])
            
div3.append(0)

for z in range(0,len(div2)):
    if z == 0:
        div3.append(div2[0])
    else:
        div3.append(div3[z]+div2[z])
       

print div2
print div3 
for n in xrange(0, numconn):
    if n%numpaths == 0:
        
        asyncoro.Coro(client, ip1, port, n)
        print "sending", n
        if n+1 < numconn:
            asyncoro.Coro(client, ip2, port, n+1)
            print "sending", n+1
        if n+2 < numconn: 
            asyncoro.Coro(client, ip3, port, n+2)
            print "sending", n+2
    port +=1

          
        
