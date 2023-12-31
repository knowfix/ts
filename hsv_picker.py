import cv2
import numpy as np
import sys
import tkinter as tk
from tkinter import filedialog

image_hsv = None
pixel = (0,0,0) #RANDOM DEFAULT VALUE

RANGE_H = 7
RANGE_S = 7
RANGE_V = 20

ftypes = [
    ("PNG", "*.png;*.PNG"),
    ("JPG", "*.jpg;*.JPG;*.JPEG"),
    ("GIF", "*.gif;*.GIF"),
    ("All files", "*.*")
]

def check_boundaries(value, tolerance, ranges, upper_or_lower):
    if ranges == 0:
        # set the boundary for hue
        boundary = 180
    else:
        # set the boundary for saturation and value
        boundary = 255

    if upper_or_lower == 1:
        value = value + tolerance
    else:
        value = value - tolerance

    if(value > boundary):
        value = boundary
    elif (value < 0):
        value = 0

    return value

def pick_color(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        pixel = image_hsv[y,x]
        print(pixel)

        #HUE, SATURATION, AND VALUE (BRIGHTNESS) RANGES. TOLERANCE COULD BE ADJUSTED.
        # Set range = 0 for hue and range = 1 for saturation and brightness
        # set upper_or_lower = 1 for upper and upper_or_lower = 0 for lower
        hue_upper = check_boundaries(pixel[0], RANGE_H, 0, 1)
        hue_lower = check_boundaries(pixel[0], RANGE_H, 0, 0)
        
        saturation_upper = check_boundaries(pixel[1], RANGE_S, 1, 1)
        saturation_lower = check_boundaries(pixel[1], RANGE_S, 1, 0)

        value_upper = check_boundaries(pixel[2], RANGE_V, 1, 1)
        value_lower = check_boundaries(pixel[2], RANGE_V, 1, 0)

        upper =  np.array([hue_upper, saturation_upper, value_upper])
        lower =  np.array([hue_lower, saturation_lower, value_lower])
        #print(lower, upper)

        #A MONOCHROME MASK FOR GETTING A BETTER VISION OVER THE COLORS 
        image_mask = cv2.inRange(image_hsv,lower,upper)
        cv2.imshow("Mask",image_mask)

        kernel = np.ones((3, 3), np.uint8)
        erosion = cv2.erode(image_mask, kernel, iterations = 2)
        dilation = cv2.dilate(erosion, kernel, iterations = 3)
        cv2.imshow("Mask 2", dilation)

def main():

    global image_hsv, pixel

    #OPEN DIALOG FOR READING THE IMAGE FILE
    root = tk.Tk()
    root.withdraw() #HIDE THE TKINTER GUI
    file_path = filedialog.askopenfilename(filetypes = ftypes)
    root.update()
    image_src = cv2.imread(file_path)
    #cv2.imshow("BGR",image_src)

    #CREATE THE HSV FROM THE BGR IMAGE
    image_hsv = cv2.cvtColor(image_src,cv2.COLOR_BGR2HSV)
    cv2.imshow("HSV",image_hsv)

    #CALLBACK FUNCTION
    cv2.setMouseCallback("HSV", pick_color)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__=='__main__':
    main()