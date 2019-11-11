from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
from math import *
import os
#from multiprocessing import Pool#

stack = []

if __name__ == "__main__":
    root = Tk()
    count = 0
    for filename in os.listdir('./test'):
        if filename.endswith(".png"): 
            print(os.path.join('./test', filename))
##            stack.append('./test/' + filename)
            exec('stack_' + str(count) + ' = ' + str('Image.open("./test/' + filename + '")'))
##            stack+count.show()
            #print(exec('stack_'+str(count)))
            stack.append(eval('stack_'+str(count)))
            count+=1
            continue
        else:
            continue
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
##    img2 = Image.open(stack[0])
##    img2.convert('RGB')
    #width = img.width()
    #height = img.height()
    canvas.create_image(0,0,image=img,anchor="nw")
    width = img.width()
    height = img.height()
    canvas.config(scrollregion=canvas.bbox(ALL))

    #function to be called when mouse is clicked
    def printcoords(event):
        #outputting x and y coords to console
        print (event.x,event.y)
    #mouseclick event
    canvas.bind("<Button 1>",printcoords)



thresh=100
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
            c = img2.getpixel((nx, ny));
            if(c < thresh and c != 255):
                frontier.append(n)
                filled_pixels.append(n)
                img2.putpixel((nx, ny), (255))
                inside += 1
    return inside, filled_pixels

def yup(x,y,z):
    count = []
    global countc
    pixely = 0
    count.append(x)
    count.append(y)
    count.append(z)
    #print('hi')
    #print(len(stack))
    while count != []:
##        print(stack[count[2]])
        if stack[count[2]].getpixel((count[0],count[1]))>thresh and stack[count[2]].getpixel((count[0],count[1]))!=254:
            stack[count[2]].putpixel((count[0],count[1]),(254))
            pixely += 1
            #print(pixely)
            if stack[count[2]].getpixel((count[0]+1,count[1]))>thresh and stack[count[2]].getpixel((count[0],count[1]))!=254:
                count.append(count[0]+1)
                count.append(count[1])
                count.append(count[2])
            if stack[count[2]].getpixel((count[0]-1,count[1]))>thresh and stack[count[2]].getpixel((count[0],count[1]))!=254:
                count.append(count[0]-1)
                count.append(count[1])
                count.append(count[2])
            if stack[count[2]].getpixel((count[0],count[1]+1))>thresh and stack[count[2]].getpixel((count[0],count[1]))!=254:
                count.append(count[0])
                count.append(count[1]+1)
                count.append(count[2])
            if stack[count[2]].getpixel((count[0],count[1]-1))>thresh and stack[count[2]].getpixel((count[0],count[1]))!=254:
                count.append(count[0])
                count.append(count[1]-1)
                count.append(count[2])
            if count[2] != 0:
                down=count[2]-1
                if stack[down].getpixel((count[0],count[1]))>thresh and stack[count[2]].getpixel((count[0],count[1]))!=254:
                    count.append(count[0])
                    count.append(count[1])
                    count.append(down)
            if count[2] != len(stack)-1:
                up=count[2]+1
                #print(count[2],up)
                if stack[up].getpixel((count[0],count[1]))>thresh and stack[count[2]].getpixel((count[0],count[1]))!=254:
                    count.append(count[0])
                    count.append(count[1])
                    count.append(up)
            #print(pixely)
        count.remove(count[0])
        count.remove(count[0])
        count.remove(count[0])
    return pixely
##    if pixely > 0:
##        print(pixely)
##    if pixely < 250 and pixely >35:
##        countc.append(x)
##        countc.append(y)
##        blue(x,y)
    #pixels=0

print('hello')
#inside, filled_pixels = floodfill(1234,1234)
pixely=yup(2315,1686,0)
print ("Inside was")
print (pixely)
print (" pixels")
##for x in range(width):
##    for y in range(height):
##        print('made it')
##        #if img2.getpixel((x,y))[0] < thresh:
##        print('started')
##        inside, filled_pixels = floodfill(x,y)
##        print ("Inside was")
##        print (inside)
##        print (" pixels")


##app = Tk()
canvas = Canvas(root)
canvas['width'] = width
canvas['height'] = height
canvas.pack()
##stack_4.show()
pimg = ImageTk.PhotoImage(image=img)
canvas.create_image(width/2, height/2, anchor='center', image=pimg)
root.mainloop()

