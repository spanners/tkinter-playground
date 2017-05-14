# File: aniwave.py
#    http://infohost.nmt.edu/tcc/help/pubs/tkinter//canvas.html#create_line

from tkinter import *
from tkinter import ttk
from demopanels import MsgPanel, SeeDismissPanel

class AnimatedWaveDemo(ttk.Frame):
    
    def __init__(self, isapp=True, name='aniwavedemo'):
        ttk.Frame.__init__(self, name=name)
        self.pack(expand=Y, fill=BOTH)
        self.master.title('Animated Wave Demo')
        self.isapp = isapp
        self._create_widgets()
        
    def _create_widgets(self):
        if self.isapp:
            MsgPanel(self, 
                     ["This demonstration contains a canvas widget with a line item ",
                      "inside it. The animation routines work by adjusting the ",
                      "coordinates list of the line; which, in turn, changes the ",
                      "position of the frequency zig-zag on the line."])
            
            SeeDismissPanel(self)
        
        self._create_demo_panel()
        
    def _create_demo_panel(self):
        demoPanel = Frame(self)
        demoPanel.pack(side=TOP, fill=BOTH, expand=Y)
        
        # Create a canvas large enough to hold the wave. In fact, the wave
        # sticks off both sides of the canvas to prevent visual glitches.
        self.__canvas = Canvas(demoPanel, width=300, height=200, background='black')
        self.__canvas.pack(padx=10, pady=10, expand=Y)
        
        # Create a coordinates list for the wave. This code does a very sketchy
        # job and relies on Tk's line smoothing to make things look better.
        self.__waveCoords = []
        for x in range(-10, 305, 5):
            self.__waveCoords.extend((x, 100))      # straight line
           
        self.__waveCoords.extend((305,0, 310, 200)) # frequency zig-zag
        
        # Create a smoothed line using the wave coordinates we've just set
        self.__canvas.create_line(self.__waveCoords, tags=('wave',), 
                                  width=1, fill='green', smooth=True)

        self.__direction = 'left'   # set the direction of wave        
        self._move()                # start the animation
                
    def _move(self):
        # start the animation
        self._basic_motion()
        self._reverse_wave()
        
        # repeat the animation every 10 milliseconds
        self.after(10, self._move)

    def _basic_motion(self):
        # Basic motion handler.
        # Advances the 'y' coordinates of the wave line
        # one step in the currently active direction.
        
        # get a copy of the current wave line coordinates
        oc = list(self.__waveCoords)    
        oclen = len(oc)
        
        for i in range(1, oclen, 2):
            if self.__direction == 'left':
                idx = i + 2
                # at a boundary?
                if idx > oclen: idx = 1 
                self.__waveCoords[i] = oc[idx]
            else:   # moving 'right'
                idx = i - 2
                # at a boundary?
                if idx < 0: idx = oclen-1   
                self.__waveCoords[i] = oc[idx]

            # redraw the wave line
            self.__canvas.coords('wave', *self.__waveCoords)
                        
    def _reverse_wave(self):
        # Oscillation handler. This detects whether to reverse the direction
        # of the wave by checking to see if the peak of the wave (whose size
        # we already know) has moved off the screen.
        
        # get current wave line coordinates
        wave = self.__canvas.coords('wave')
        if wave[1] < 10:    # first 'y' coord
            self.__direction = 'right'
        elif wave[-1] < 10: # last 'y' coord
            self.__direction = 'left'

if __name__ == '__main__':
    AnimatedWaveDemo().mainloop()