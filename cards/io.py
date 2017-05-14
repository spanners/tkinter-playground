"""
The only safe way to deal with communication between threads is via a Queue.
This pcakage encapsulates the creation of clients and servers and provides
reliable communication via a queue.

This IO class supports 3 uses:
   a) a simple client
   b) a server that starts several clients
   c) a client started by a server
"""

import os
try:
    from Queue import Queue, Empty
except:
    from queue import Queue, Empty
from time import sleep
from threading import Thread
import socket
from socket import gethostname

class IO(object):
    """
    A general IO class providing a socket a queue and a thread.
    With 3 user methods get, put and quit.
    messages are passed out through a queue.
    messages are pased as tuples and have
    message name, sender and message arguments.
    sender.put can be used to send messages in reply.
    The following messages are emitted by the process:
       started_msg
       finished_msg
    """
    
    def __init__(self, socket=None, queue=None, name=None, host=None, port=None):
        """
        Create thread with name, socket and queue.
        """
        self.name = name or '?'
        self._socket = socket
        self._queue = queue
        self._host = host or os.environ.get('IOHOST', '') or gethostname()
        self._port = port or os.environ.get('IOPORT', '')
        self._working = True
        self._queue = queue or Queue()
        t = Thread(target=self._work)
        t.setDaemon(True)
        t.start()

    def __repr__(self):
        """
        """
        return self.name
    
    def put(self, *a):
        """
        Send a message via the socket.
        """
        print('put', self.name, a)
        data = ','.join([str(x) for x in a])+';'
        try:
            self._socket.send(data)
        except:
            self._socket.send(data.encode())

    def get(self):
        """
        Receive a message from the queue.
        """
        try:
            result = self._queue.get(block=False)
            print('get', result)
            return result
        except Empty as msg:
            return None

    def quit(self):
        """
        """
        # print 'quit'
        self._working = False

    def _qput(self, *a):
        """
        Send a message through the queue.
        Pass self so receiver can reply.
        """
        #print 'queue-put', a
        print("%s putting message %s on its queue" % (self, (self,)+a))
        self._queue.put((self,)+a)
        
    def _work(self):
        """
        This is where the work happens...
        Connect if no socket, read until done, disconnect.
        Pass status mesasges and received messages + args into the queue.
        Received messages are comma delimited and semicolon terminated.
        """
        qput = self._qput
        s = self._socket
        if not s: # may already exist
            self._socket = s = self._connect()
            if not s:
                qput('finished_msg')
                return
        qput('started_msg', self._host, self._port)
        s.setblocking(1)
        s.settimeout(0.1)
        d = ''
        print("self._working", self._working)
        while self._working:
            try:
                d += s.recv(1) # poor performance simple code
                print("Got d %s" % d.decode())
            except Exception:
                continue
            if d.endswith(';'):
                d = d.decode()
                print("d is %s" % d)
                if d=='bye_msg;':
                    break
                print("d becomes %s" % (d[:-1].split(',')))
                qput(*d[:-1].split(','))
                d = ''
        self.put('bye_msg')
        s.close()
        qput('finished_msg')

 
class ClientIO(IO):
    """
    An IO class for a client.
    """

    def _connect(self):
        """
        Wait for a server.
        If failing to connect then try first few ip's of lan. 
        """
        HOST = IOHOST = self._host
        PORT = self._port
        while self._working:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                print('trying to connect to %s@%s' %  (HOST, PORT))
                s.connect((HOST, PORT))
                self._host = HOST
                print('connected to %s@%s' %  (HOST, PORT))
                return s
            except socket.error as msg:
                self._qput('error_msg', str(msg))
                sleep(1.0)
                if HOST == IOHOST:
                    HOST = '192.168.0.2' # try LAN
                elif HOST == '192.168.0.9':
                    HOST = IOHOST # check expected host
                else: # increment ip on LAN
                    HOST = HOST[:-1]+str(int(HOST[-1])+1)

class ServerIO(IO):
    """
    An IO class for a server.
    """

    def _work(self):
        """
        A servers job is to start client threads as they arrive.
        Clients have a ready made socket and queue.
        """
        serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            serversock.bind((self._host, self._port))
        except Exception as e:
            print("self._host", self._host, "self._port", self._port)
            raise e
        serversock.listen(10)
        while self._working:
            (clientsock, _) = serversock.accept()
            IO(socket=clientsock, queue=self._queue) # both socket and queue already exist
