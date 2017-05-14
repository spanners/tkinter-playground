"""
The idea is to create a gui object that can front either a client (1 source)
or a server (several sources).

Messages are handled as methods... I like that!

A Tk GUI that receives input from somewhere: via io.get().
The received messages are either None or tuples with method name and parameters.
The first parameters is always the sender (which may be used to reply via sender.put()).
Other parameters are optional.
Messages put are the same format: method name followed by optional parameters.
3 internal messages are always provided: _started_msg, _ended_msg and _error_msg.
Valid messages are introduced viw the message decorator.
"""

try:
    from Tkinter import Tk
except:
    from tkinter import Tk

from functools import wraps

def message(method):
    """
    Decorator for message methods.
    Add the message into the list of expected messages.
    """
    message.messages.add(method.__name__)
    @wraps(method)
    def decorated(self, sender, *args):
        method(self, sender, *args)
    return decorated
message.messages = set()

class IOGui(object):
    """
    A gui with simple comms interface.
    """
    
    def __init__(self, io):
        """
        """
        self._pending_quit = False
        self._io = io
        self._root = Tk()
        self._root.title('%s %s@%s' % (io.name, io._host, io._port))
        self._root.protocol('WM_DELETE_WINDOW', self._delete_window)
        self.create_widgets()
        self._suspend()
        self._root.mainloop()

    def _delete_window(self):
        """
        Tell the io to stop.
        Note: do not quit until the io reports finished (unless the io seems to be stuck).
        """
        if self._pending_quit:
            self._cleanup()
        else:
            self._pending_quit = True
            self._io.quit()
        
    def _cleanup(self):
        """
        Tidy up and go!
        """
        if self._suspended:
            self._root.after_cancel(self._suspended)
        self._root.quit()
        
    def _suspend(self):
        """
        Short delay before checking the queue again.
        """
        self._suspended = self._root.after(20, self._check_io)
        
    def _check_io(self):
        """
        read all messages from io and pass on as methods
        """
        self._suspended = None
        while True:
            data = self._io.get()
            if not data:
                self._suspend()
                return
            sender = data[0]
            method = data[1]
            if method in message.messages:
                getattr(self, method)(sender, *data[2:])
            else:
                print('missing method for message', data)

    @property
    def root(self):
        """
        """
        return self._root
    
    @message
    def error_msg(self, sender, msg):
        """
        Called to report errors.
        """
        print('roll your own error_msg handler', sender, msg)

    @message
    def started_msg(self, sender, host, port):
        """
        Called whenever a connection is made.
        """
        print('roll your own started_msg handler', sender, host, port)

    @message
    def bye_msg(self, sender):
        """
        Called just before a connection is broken.
        """
        print('roll your own bye_msg handler', sender)

    @message
    def finished_msg(self, sender):
        """
        Called whenever a connection is broken.
        If you roll your own be sure to call this one when all is done.
        """
        self._cleanup()
