import os
from queue import Queue
from queue import Empty
from time import sleep
from threading import Thread
import socket
from socket import gethostname


MSG_ENCODING = 'utf-8'
STARTED_MSG = 'started_msg'
BYE_MSG = 'bye_msg;'



class IO(object):
    """
    Provides a socket, a queue, and a thread.
    With 3 user methods get, put and quit.
    Messages are passed out through a queue.
    Messages are passed as tuples and have
    message name, sender, and message arguments.
    sender.put can be used to send messages in reply.
    The following messages are emitted:
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
        #t.setDaemon(True)
        t.start()

    def __repr__(self):
        """
        """
        return self.name

    @staticmethod
    def _encode_msg_tuple(*t):
        """
        Messages are comma delimited and semicolon terminated.
        Messages are encoded in utf-8.
        """
        formatted_string = ','.join([str(x).lstrip() for x in t])+';'
        return formatted_string.encode(MSG_ENCODING)

    @staticmethod
    def _split_msg_string(s):
        s = s.replace('"','')
        s = s.replace('(', '')
        s = s.replace(')', '')
        s = s.replace("'", '')
        s = s.lstrip()
        s = s[:-1].split(',')
        return s

    @staticmethod
    def _decode_msg_string(s):
        return s.decode(MSG_ENCODING)

    def put(self, *a):
        """
        Send a message via the socket.
        """
        data = IO._encode_msg_tuple(a)
        self._socket.send(data)

    def get(self):
        """
        Receive a message from the queue.
        """
        try:
            result = self._queue.get(block=False)
            return result
        except Empty as msg:
            return None

    def quit(self):
        """
        """
        self._working = False

    def _qput(self, *a):
        """
        Send a message through the queue.
        Pass self so reciever can reply.
        """
        self._queue.put((self,)+a)

    def _work(self):
        """
        This is where the work happens...
        Connect if no socket, read until done, disconnect.
        Pass status messages and recieved messages + args into the queue.
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
        d = bytearray()
        while self._working:
            try:
                d.extend(s.recv(1)) # poor performance simple code
            except Exception as _:
                continue
            if (IO._decode_msg_string(d)).endswith(';'):
                if IO._decode_msg_string(d) == BYE_MSG:
                    break
                print("Putting decoded msg string onto queue", IO._split_msg_string(IO._decode_msg_string(d)))
                qput(*IO._split_msg_string(IO._decode_msg_string(d)))
                d = bytearray()
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
        """
        HOST = IOHOST = self._host
        PORT = self._port
        while self._working:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                print('trying to connect to %s@%s' % (HOST, PORT))
                s.connect((HOST, PORT))
                self._host = HOST
                print('connected to %s@%s' % (HOST, PORT))
                return s
            except socket.error as msg:
                self._qput('error_msg', str(msg))
                sleep(1.0)

class ServerIO(IO):
    """
    An IO class for a server.
    """

    def __init__(self, **args):
        super(ServerIO, self).__init__(**args)

    def _work(self):
        """
        A servers job is to start client threads as they arrive.
        Clients have a ready made socket and queue.
        """

        serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversock.bind((self._host, self._port))
        serversock.listen(10)
        while self._working:
            (clientsock, _) = serversock.accept()
            IO(socket=clientsock, queue=self._queue) # both socket and queue already exist
