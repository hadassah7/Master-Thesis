import socket, sys, asyncoro, ntplib, time

list2 = []
number = 0
size = 0
count = 0
def currenttime():
    c = ntplib.NTPClient()
    response = c.request('pool.ntp.org')
    return response.tx_time
def process(conn, addr, sock, coro=None):
    data = ''
    final = ''
    global number
    global list2
    global size
    global count
    
    while True:
        data = yield conn.recv_msg()
        print data
        if data == 'terminate':
            break 
        #print count, size
        size += len(data)
        list1 = data.split(':data', 2 ) 
        var1 = int(list1[0])
        print "This is", var1
        numchunks = int(list1[1])
        print "Total number of chunks", numchunks
        print "Number is", count
        if count == 0:
            list2 = [None]* numchunks
            print 'empty array created'
        count += 1
        list3 = list1[2].split(' ',1)
        print list3
        if list2[var1] == None:
            list2[var1] = list3[1]
        if list2.count(None) == 0:
            
            for n in range(0, len(list2)):
                final += list2[n]
            print 'size:', len(final)
            print 'size of data', len(data)
            file1 = open(list3[0],'wb')
            file1.write(final)
            
            break
            
    #conn.send(var1)       
    conn.close()
    
    #print data
        
    
def server_proc(host, port, coro=None):
    global count1
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock = asyncoro.AsyncSocket(sock)
    try:
        yield sock.bind((host, port))
    except socket.error as msg:
        print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()
    print 'Socket bind complete'
    sock.listen(1280)
    print 'Socket now listening'
    count1 = 0
    while True:
        conn, addr = yield sock.accept()
        print 'Connected with ' + addr[0] + ':' + str(addr[1])
        if count1 ==0:
            #rt1 = currenttime()
            rt1 = time.time()
            print rt1
        count1 += 1
        asyncoro.Coro(process, conn, addr, sock)
        
        
    sock.close()
asyncoro.Coro(server_proc, '', 8012)
