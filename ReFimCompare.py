import random
from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
import time

version = "1.4"
print("version: " + str(version))
# Import libraries & version
print("No error handling, I expect you to be smart")

rv = 0
gv = 0
bv = 0
choice = 0
i = 0
# initializing variables 

def op_imageSelect():
    global groundTruth
    groundTruth = Tk()
    groundTruth.call('wm', 'attributes', '.', '-topmost', True)
    groundTruth.filename = filedialog.askopenfilename(initialdir="/", title="Please Select Ground Truth Image")
    # User selects ground truth image
    
    global lowSample
    lowSample = Tk()
    lowSample.filename = filedialog.askopenfilename(initialdir="/", title="Please Select Low Sample Image")
    # User selects low sample image
    
    global Image1
    global Image2

    Image1 = Image.open(str(groundTruth.filename))
    Image2 = Image.open(str(lowSample.filename))
    
    Image1 = Image1.convert('RGB')
    Image2 = Image2.convert('RGB')
    
    
    lowSample.destroy()
    groundTruth.destroy()
    
    # load the photos
    global x
    global y
    x, y = Image1.size
    global pixel_total
    pixel_total = x * y




def op_total(rv, bv, gv):
    start_time = time.time()
    rv = 0
    gv = 0
    bv = 0
    xc = 1
    yc = 1
    i = x
    # current values for x and y
    # if i is less then x the program crashes, I have no clue

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

    global total_time
    total_time = (time.time() - start_time)

    return (rv, gv, bv)

def op_results():
    print("\nfiles compared: ")
    print(str(groundTruth.filename))
    print(str(lowSample.filename))
    print("")


    print("total execution time ")
    print(str(round(total_time, 4)) + " seconds")

    print("Total Pixels Sampled: " + str("{:,}".format(pixel_total)))
    print("")

    print("Red Variance: " + (str(round(rv / pixel_total, 2))))
    print("Green Variance: " + (str(round(gv / pixel_total, 2))))
    print("Blue Variance: " + (str(round(bv / pixel_total, 2))))
    print("")

    print("Mean RGB Variance: " + (str(round((rv / pixel_total + gv / pixel_total + bv / pixel_total) / 3, 2))))
    # dividing gross rgb values by the number of samples, creating a mean average.
    # rounds and prints the results
    


#op_imageSelect()        
         
while choice != 4:
    print("\n\nPlease choose a operating mode \n")
    choice = int(input("Enter 1 for ImageSelect, 2 for Scan, 3 for Show Results, 4 for quit\n"))
    if choice == 1:
        op_imageSelect()
        print ("1")
    elif choice == 2:
        rv, gv, bv = op_total(rv, gv, bv)
    elif choice == 3:
        op_results()
    else:
        break


quit()
     

