Learn more or give us feedback
import random
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class AutoScrollbar(ttk.Scrollbar):
    ''' A scrollbar that hides itself if it's not needed.
        Works only if you use the grid geometry manager '''
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.grid_remove()
        else:
            self.grid()
        ttk.Scrollbar.set(self, lo, hi)

    def pack(self, **kw):
        raise tk.TclError('Cannot use pack with this widget')

    def place(self, **kw):
        raise tk.TclError('Cannot use place with this widget')

class Zoom(ttk.Frame):
    ''' Simple zoom with mouse wheel '''
    def __init__(self, mainframe, path):
        ''' Initialize the main Frame '''
        ttk.Frame.__init__(self, master=mainframe)
        self.master.title('Trace Project')
        # Vertical and horizontal scrollbars for canvas
        vbar = AutoScrollbar(self.master, orient='vertical')
        hbar = AutoScrollbar(self.master, orient='horizontal')
        vbar.grid(row=0, column=1, sticky='ns')
        hbar.grid(row=1, column=0, sticky='we')
        # Open image
        self.image = Image.open(path)
        # Create canvas and put image on it
        self.canvas = tk.Canvas(self.master, highlightthickness=0,
                                xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        self.canvas.grid(row=0, column=0, sticky='nswe')
        vbar.configure(command=self.canvas.yview)  # bind scrollbars to the canvas
        hbar.configure(command=self.canvas.xview)
        # Make the canvas expandable
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        # Bind events to the Canvas
        self.canvas.bind('<ButtonPress-3>', self.move_from)
        self.canvas.bind('<B3-Motion>',     self.move_to)
        root.bind('<Up>',self.new_img)
        root.bind('<Key>', self.wheel)
        self.canvas.bind('<MouseWheel>', self.wheel)  # with Windows and MacOS, but not Linux
        self.canvas.bind('<Button-5>',   self.wheel)  # only with Linux, wheel scroll down
        self.canvas.bind('<Button-4>',   self.wheel)  # only with Linux, wheel scroll up
        # Show image and plot some random test rectangles on the canvas
        self.imscale = 1.0
        self.imageid = None
        self.delta = 0.75
        width, height = self.image.size
        minsize, maxsize = 5, 20
        for n in range(10):
            x0 = random.randint(0, width - maxsize)
            y0 = random.randint(0, height - maxsize)
            x1 = x0 + random.randint(minsize, maxsize)
            y1 = y0 + random.randint(minsize, maxsize)
            color = ('red', 'orange', 'yellow', 'green', 'blue')[random.randint(0, 4)]
            self.canvas.create_rectangle(x0, y0, x1, y1, outline='black', fill=color,
                                         activefill='black', tags=n)
        # Text is used to set proper coordinates to the image. You can make it invisible.
        self.text = self.canvas.create_text(0, 0, anchor='nw', text='Scroll to zoom')
        self.show_image()
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
##    def test(self, event):
##        print(event.char)

    def move_from(self, event):
        ''' Remember previous coordinates for scrolling with the mouse '''
        print(event.x,event.y)
        self.canvas.scan_mark(event.x, event.y)
        MousePressX=event.x
        MousePressY=event.y

    def move_to(self, event):
        ''' Drag (move) canvas to the new position '''
        self.canvas.scan_dragto(event.x, event.y, gain=1)
        MouseReleaseX=event.x
        MouseReleaseY=event.y
        FinalPositionX= MousePressX- MouseReleaseX
        FinalPositionY= MousePressY- MouseReleaseY

    def wheel(self, event):
        ''' Zoom with mouse wheel '''
        scale = 1.0
        # Respond to Linux (event.num) or Windows (event.delta) wheel event
        if event.num == 5 or event.delta == -120 or event.char=='-':
            scale        *= self.delta
            self.imscale *= self.delta
        if event.num == 4 or event.delta == 120 or event.char=='+':
            scale        /= self.delta
            self.imscale /= self.delta
        # Rescale all canvas objects
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        self.canvas.scale('all', x, y, scale, scale)
        self.show_image()
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
    def new_img(self, event):
        print(event.char)
        app=Zoom(root, path="B1run02_png/B1_Run02_BSED_slice_0022.png")
        #Add the position to load FinalPositionX, FinalPositionY##########################
        
    def show_image(self):
        ''' Show image on the Canvas '''
        if self.imageid:
            self.canvas.delete(self.imageid)
            self.imageid = None
            self.canvas.imagetk = None  # delete previous image from the canvas
        width, height = self.image.size
        new_size = int(self.imscale * width), int(self.imscale * height)
        imagetk = ImageTk.PhotoImage(self.image.resize(new_size))
        # Use self.text object to set proper coordinates
        self.imageid = self.canvas.create_image(self.canvas.coords(self.text),
                                                anchor='nw', image=imagetk)
        self.canvas.lower(self.imageid)  # set it into background
        self.canvas.imagetk = imagetk  # keep an extra reference to prevent garbage-collection


    def floodfill(img_x, img_y):
        inside = 1
        filled_pixels = [(img_x, img_y)] #paint them after
        frontier = [(img_x,img_y)];
        while len(frontier) > 0:
            img_x, img_y = frontier.pop()
            neighbors = [
                    (img_x + 1,img_y),
                    (img_x - 1,img_y),
                    (img_x, img_y + 1),
                    (img_x, img_y - 1)
                    ];
            for n in neighbors:
                nx, ny = n
                if nx < 0 or nx >= width:
                    continue
                if ny < 0 or ny >= height:
                    continue
                c = pic.getpixel((nx, ny));
                if(c < thresh and c != 255):
                    frontier.append(n)
                    filled_pixels.append(n)
                    pic.putpixel((nx, ny), (255))
                    inside += 1
        return inside, filled_pixels

    if("<Button 3>"==True):
        floodfill(event.x, event.y)



path = 'B1_Run02_BSED_slice_0021.png'  # place path to your image here
root = tk.Tk()
app = Zoom(root, path=path)
width, height = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry('%dx%d+0+0' % (width,height))
root.mainloop()
