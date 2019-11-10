from Tkinter import *
from tkFileDialog import askopenfilename
import Image, ImageTk
from math import *
#from multiprocessing import Pool#

if __name__ == "__main__":
    root = Tk()

    #setting up a tkinter canvas with scrollbars
    frame = Frame(root, bd=2, relief=SUNKEN)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    xscroll = Scrollbar(frame, orient=HORIZONTAL)
    xscroll.grid(row=1, column=0, sticky=E+W)
    yscroll = Scrollbar(frame)
    yscroll.grid(row=0, column=1, sticky=N+S)
    canvas = Canvas(frame, bd=0, xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
    canvas.grid(row=0, column=0, sticky=N+S+E+W)
    xscroll.config(command=canvas.xview)
    yscroll.config(command=canvas.yview)
    frame.pack(fill=BOTH,expand=1)

    #adding the image
    File = askopenfilename(parent=root, initialdir="C:/",title='Choose an image.')
    img = ImageTk.PhotoImage(Image.open(File))
    canvas.create_image(0,0,image=img,anchor="nw")
    canvas.config(scrollregion=canvas.bbox(ALL))

    #function to be called when mouse is clicked
    def printcoords(event):
        #outputting x and y coords to console
        print (event.x,event.y)
    #mouseclick event
    canvas.bind("<Button 1>",printcoords)

    root.mainloop()



def floodfill(img_x, img_y):
    inside = 1
    filled_pixels = [(img_x, img_y)]
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
            if(c[0] < thresh and c[0] != 255):
                frontier.append(n)
                filled_pixels.append(n)
                pic.putpixel((nx, ny), (255, 255, 255))
                inside += 1
    return inside, filled_pixels


for x in range(width):
	for y in range(height):
		if pic.getpixel((x,y))[0] < thresh:
			inside, filled_pixels = floodfill(x,y)
			print "Inside was"
			print inside
			print " pixels"


app = Tk()
canvas = Canvas(app)
canvas.pack()
canvas['width'] = width
canvas['height'] = height
pimg = ImageTk.PhotoImage(image=pic)
canvas.create_image(width/2, height/2, anchor='center', image=pimg)
app.mainloop()
