""" 
# UDPPacketGrabber Grabs UDP packets that it is sent, and puts them on a queue
# WidgetUpdater gets messages off this queue and draws onto a widget

# To test:
# 1. In one command line window, run `python udp_packet_grabber.py`
# 2. In another command line window, run `python` and type the following:
>>> from socket import socket, AF_INET, SOCK_DGRAM
>>> s = socket(AF_INET, SOCK_DGRAM)
>>> s.sendto(b'Hello, world!', ('localhost', 20000))
"""

from socket import socket
from socket import AF_INET
from socket import SOCK_DGRAM

import threading
import queue as Queue

import tkinter as Tk
import tkinter.constants as TkConst


LARGE_FONT = ("Verdana", 12)


class UDPPacketGrabber(threading.Thread):

    def __init__(self, address, lock, queue):
        threading.Thread.__init__(self)

        self.lock = lock # threading.Lock
        self.queue = queue # Queue.Queue

        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.bind(address)

    def run(self):
        while True:
            msg, addr = self.sock.recvfrom(8192)
            with self.lock:
                self.queue.put(msg)


class WidgetUpdater(object):

    def __init__(self, root, lock, queue, widget):
        self.root = root # Tkinter window
        self.lock = lock # threading.Lock
        self.queue = queue # Queue.Queue
        self.widget = widget # Tkinter widget

    def get_from_queue_and_redraw_widget(self):
        if not self.queue.empty():
            with self.lock:
                msg = self.queue.get()
                self.widget.set(msg)
        self.root.after(10, self.get_from_queue_and_redraw_widget)


class Application(Tk.Tk):
    
    def __init__(self, *args, **kwargs):
        Tk.Tk.__init__(self, *args, **kwargs)
        container = Tk.Frame(self)

        container.pack(side=TkConst.TOP, fill=Tk.BOTH, expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        frame = StartPage(container, self)

        self.frames[StartPage] = frame

        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)


    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


class StartPage(Tk.Frame):

    def __init__(self, parent, controller):
        Tk.Frame.__init__(self, parent)
        label = Tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack()



def main():
    top = Tk.Tk()
    queue = Queue.Queue()
    v = Tk.StringVar()
    label = Tk.Label(top, textvariable=v)
    lock = threading.Lock()
    label.pack(fill=TkConst.BOTH, side=TkConst.LEFT, padx=15, pady=15, expand=True)

    o = WidgetUpdater(top, lock, queue, widget=v)

    address = ('localhost', 20000)
    grabber = UDPPacketGrabber(address=address, lock=lock, queue=queue)
    grabber.start()


    top.after(10, o.get_from_queue_and_redraw_widget)
    top.mainloop()
    grabber.join()


if __name__ == '__main__':
    app = Application()
    app.mainloop()
