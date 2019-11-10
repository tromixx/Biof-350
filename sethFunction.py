#Save x and y position after doing click in the black image generated
#Also creates the 8 variables to determinate position

#We are going to need 
# 1. Find Center point
# 2. Flood FIll

#Put proper pictures
#Background things and Promote stuff! (Promote on google, Right description for each page, )
#Ideas(Profile Picture)

from PIL import Image,ImageTk
from math import *
from commands import getoutput
from Tkinter import Tk,Canvas
from multiprocessing import Pool

pic = Image.open("start.png").convert("RGB")

width, height = pic.size
print width, height

thresh = 130
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


#com
def check_roundness(filled_pixels):
    xmax = 0
    xmin = width
    ymax = 0
    ymin = height
    for pix in filled_pixels:
        x,y = pix
        if x > xmax: xmax = x
        if x < xmin: xmin = x
        if y > ymax: ymax = y
        if y < ymin: ymin = y
    yextent = ymax - ymin
    xextent = xmax - xmin
    diameter_estimate = (yextent + xextent) / 2
    if(diameter_estimate == 0):
        return False
    area_estimate = 3.141592653 * ((diameter_estimate/2)**2)
    unroundness = abs(float(area_estimate) - len(filled_pixels)) / len(filled_pixels)
    print unroundness
    if(unroundness > 0.6):
        return False
    xc = (xmax + xmin)/2
    yc = (ymax + ymin)/2
    max_radius = 0
    for pix in filled_pixels:
        x,y = pix
        dist = sqrt((x-xc)**2 + (y-yc)**2)
        if dist > max_radius: max_radius = dist
    xy_skew = abs(float(yextent) - xextent) / diameter_estimate
    other_skew = abs(float(max_radius) - diameter_estimate/2) / diameter_estimate
    skewness = xy_skew + other_skew
    print skewness
    if other_skew > 0.12:
        return True
#com


def highlight_boundaries():
    global pic
    new_image = Image.new("RGB", (width, height))
    newpix = new_image.load()
    for x in range(2, width-2):
        for y in range(2, height - 2):
            neighbors = [
                (x + 1,y),
                (x - 1,y),
                (x, y + 1 ),
                (x, y - 1 ),
                (x + 2,y),
                (x - 2,y),
                (x, y + 2 ),
                (x, y - 2 ),
                (x + 1,y + 1),
                (x - 1,y - 1),
                (x - 1, y + 1 ),
                (x + 1, y - 1 )
                ];
            nvals = [pic.getpixel((n[0], n[1]))[0]   for n in neighbors]
            our_color = pic.getpixel((x, y))[0]
            navg = sum(nvals)/len(nvals)
            diff = sum([abs(nv - navg) for nv in nvals]) / 3
            newcolor = -100 + our_color + diff
            newpix[x,y] = (newcolor, newcolor, newcolor)
            #newpix[x,y] = diff
            if(newpix[x,y][0] < 0):
                newpix[x,y] = (0, 0, 0)
            if(newpix[x,y][0] > 255):
                newpix[x,y] = (255, 255, 255)
    pic = new_image

#highlight_boundaries()


count = 0;
for x in range(width):
    for y in range(height):
        if pic.getpixel((x,y))[0] < thresh:
            inside, filled_pixels = floodfill(x,y)
            print "Inside was ", inside, " pixels"
            if inside > 5:
                if check_roundness(filled_pixels):
                    count += 1
                    for pix in filled_pixels:
                        pic.putpixel(pix, (182, 0, 255))

print count

app = Tk()
canvas = Canvas(app)
canvas.pack()
canvas['width'] = width
canvas['height'] = height
pimg = ImageTk.PhotoImage(image=pic)
canvas.create_image(width/2, height/2, anchor='center', image=pimg)
app.mainloop()



#Kent Flood fill
def yup(x,y):
    count = []
    global countc
    pixely = 0
    count.append(x)
    count.append(y)
    #print('hi')
    while count != []:
        if newim.getpixel((count[0],count[1]))==(0,0,0):
            newim.putpixel((count[0],count[1]),(255,0,0))
            pixely += 1
            #print(pixels)
            if newim.getpixel((count[0]+1,count[1]))==(0,0,0):
                count.append(count[0]+1)
                count.append(count[1])
            if newim.getpixel((count[0]-1,count[1]))==(0,0,0):
                count.append(count[0]-1)
                count.append(count[1])
            if newim.getpixel((count[0],count[1]+1))==(0,0,0):
                count.append(count[0])
                count.append(count[1]+1)
            if newim.getpixel((count[0],count[1]-1))==(0,0,0):
                count.append(count[0])
                count.append(count[1]-1)
            #print(pixely)
        count.remove(count[0])
        count.remove(count[0])


#Draw a line
from tkinter import *

def draw_line(event):
    global click_number
    global x1,y1
    if click_number==0:
        x1=event.x
        y1=event.y
        click_number=0

my_window = Tk()
my_canvas = Canvas(my_window, width=400, height=400, background='white')
my_canvas.grid(row=0,column=0)
my_canvas.bind('<Button-1>',draw_line)
click_number=0
my_window.mainloop()



#Final Flood fill
from tkinter import *

def draw_line(event):
    global click_number
    global x1,y1
    if click_number==0:
        x1=event.x
        y1=event.y
        click_number=0

my_window = Tk()
my_canvas = Canvas(my_window, width=400, height=400, background='white')
my_canvas.grid(row=0,column=0)
my_canvas.bind('<Button-1>',draw_line)
click_number=0
my_window.mainloop()
