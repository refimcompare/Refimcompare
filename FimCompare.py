import random
from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog

version = "1.2b"
# Import libraries
print("version: " + str(version))

groundTruth = Tk()
groundTruth.filename = filedialog.askopenfilename(initialdir="/", title="Please Select Ground Truth Image")
# User selects ground truth image

lowSample = Tk()
lowSample.filename = filedialog.askopenfilename(initialdir="/", title="Please Select Low Sample Image")
# User selects low sample image


Image1 = Image.open(str(groundTruth.filename))
Image2 = Image.open(str(lowSample.filename))
# load the photos

x, y = Image1.size

# find the resolution / only works if both are the same size

# gross R,G,B values collected over each sample
rv = 0
gv = 0
bv = 0
choice = 0
i = 0
pixel_total = x * y
print (pixel_total)
# index
def op_info():
        print("Sample takes random samples from the reference, and cross references its image pair. Fast but can lack accuracy")
        print("Total analyses every pixel from both images using a systemic approach. Slow but accurate")

def op_sample():

    print("total size in pixels: " + str(x * y))
    pixel_total = int(input("samplesize in pixles: "))
    # user picks a sample, total size is given to help determine scale
    i = 0
    rv = 0
    gv = 0
    bv = 0

    while i < pixel_total:
            
        rx = random.randint(0 + 1, x - 1)
        ry = random.randint(0 + 1, y - 1)
        # finds a x, y coordinate

        r, g, b = Image1.getpixel((rx, ry))
        rc, gc, bc = Image2.getpixel((rx, ry))
        # both images get sampled at that coordinate

        rv = rv + abs(rc - r)
        gv = gv + abs(gc - g)
        bv = bv + abs(bc - b)
        # r and rc(red and red copy are temporary values,
        # as such they combine into RV which is gross/total.

        if i % (pixel_total / 8) == 0:
            print(str(round((i + 1) / pixel_total * 100)) + "%")
        i = i + 1
        # counter iterates
    return (rv, gv, bv)
def op_total(rv, bv, gv):
    xc = 1
    yc = 1
    i = x
    # current values for x and y
    # if i is less then 1920 the program crashes, I have no clue

    while i < pixel_total:
        while xc < x:
            r, g, b = Image1.getpixel((xc, yc))
            rc, gc, bc = Image2.getpixel((xc, yc))

            rv = rv + abs(rc - r)
            gv = gv + abs(gc - g)
            bv = bv + abs(bc - b)

            xc = xc + 1
            i = i + 1

        xc = 1
        yc = yc + 1
        i = i + 1
        if i % (pixel_total / 100) == 0:
            print(str(round((i + 1) / pixel_total * 100)) + "%")
    return (rv, gv, bv)

# ra = float(rv/pixel_total)
# ga = float(gv/pixel_total)
# ba = float(bv/pixel_total)
# gross value / number of samples for the final value
# legacy code that I am afraid to delete,


        
                


while choice != 5:
    print("Please choose a operating mode")
    choice = int(input("Enter 1 for Sample, 2 for Total, 3 for more Info, 4 for Show Results, "))
    if choice == 1:
        rv, gv, bv = op_sample()
    elif choice == 2:
        rv, gv, bv = op_total(rv, gv, bv)
    elif choice == 3:
        op_info()
    else:
        break

print("\nfiles compared: ")
print(str(groundTruth.filename))
print(str(lowSample.filename))
print("")

print("Total Pixels Sampled: " + str("{:,}".format(pixel_total)))
print("")

print("Red Variance: " + (str(round(rv / pixel_total, 2))))
print("Green Variance: " + (str(round(gv / pixel_total, 2))))
print("Blue Variance: " + (str(round(bv / pixel_total, 2))))
print("")

print("Mean RGB Variance: " + (str(round((rv / pixel_total + gv / pixel_total + bv / pixel_total) / 3, 2))))
# dividing gross rgb values by the number of samples, creating a mean average.
# rounds and prints the results

print("")
input("enter anything to quit: \n\n")
quit()
     

