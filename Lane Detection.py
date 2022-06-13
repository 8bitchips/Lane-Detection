import time
import cv2
import numpy as np
import matplotlib.pyplot as plt


def make_coordinates(image, line_parameters):
    global x1,y1,x2,y2
    slope, intercept = line_parameters
    y1 =  image.shape[0]
    y2 = int(y1 * (3/5))                  #y1*(3/5) is done so that the line is drawn till (3/5)th of the whole image.
    x1 = int((y1 - intercept)/slope)
    x2 = int((y2 - intercept)/ slope)
    print('(',x1,',',y1,')', '(',x2,',',y2,')')
    return np.array([x1, y1, x2, y2])


def average_slope_intercepts(image, lines):
    #global x1, y1, x2, y2
    left_fit = []
    right_fit = []
    print(" ")
    print("   Left Fit     Right Fit")
    print('(  x1 ,  y1 ) (  x2 ,  y2 )')
    #print("Parameters ")
    #print("Image : ", image)
    #print("Lines : ", lines)
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        #print(x1, y1, x2, y2)
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        #print(parameters)
        slope = parameters[0]
        intercept = parameters[1]
        #print("Slope : ", slope)
        #print("Intercept : ", intercept)
        if slope < 0:
            left_fit.append((slope, intercept))
        else:
            right_fit.append((slope, intercept))
    #print("Left Fit Slope  : ", left_fit[0], end="\n")
    #print("Right Fit Slope : ", right_fit[0], end="\n")
    left_fit_average = np.average(left_fit, axis=0)
    right_fit_average = np.average(right_fit, axis=0)
    #print("Left : ",left_fit_average)
    #print("Right : ", right_fit_average)
    left_line = make_coordinates(image, left_fit_average)
    right_line = make_coordinates(image, right_fit_average)
    return np.array([left_line, right_line])


def canny1(image):
    global gray, blur, canny
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5), 0)
    canny =  cv2.Canny(blur, 50, 100)
    return canny1



def region_of_interest(image):
    height = image.shape[0]
    traingle = np.array([[(200, height), (1100, height), (550, 250)]])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, traingle, 255)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image


def display_lines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for x1, y1, x2, y2 in lines:
            cv2.line(line_image, (x1,y1), (x2,y2), (255, 0, 0), 10)
    return line_image


"""test_image = cv2.imread('test_lane_image.png')
#test_image1 = cv2.imread('difficult_lane_test_image.png')
test_image = cv2.resize(test_image, (1280, 720))
lane_image = np.copy(test_image)
canny_image = canny1(lane_image)
cropped_image = region_of_interest(canny)
hough_lines = cv2.HoughLinesP(cropped_image, 2, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap=5)
averaged_lines = average_slope_intercepts(lane_image, hough_lines)
line_image = display_lines(lane_image, averaged_lines)
blend_image = cv2.addWeighted(lane_image, 0.8, line_image, 1, 1)
cv2.imshow("result", blend_image)
cv2.waitKey(0)
#print("Starting Coodinates : ", x1, y1)
#print("Ending Coordinates  : ", x2, y2)
#plt.plot((x1,y1),(x2,y2), marker='o', markerfacecolor='r', label="Starting Coordinates", color='blue')
#plt.plot((340, 654), (454, 472), marker='o', markerfacecolor='r', label="Ending Coordinates", color='blue')
#plt.plot((607, 325), (705, 426), marker='o', markerfacecolor='r', label="Ending Coordinates", color='blue')
#plt.plot((592, 316), (685, 412), marker='o', markerfacecolor='r', label="Ending Coordinates", color='blue')
#plt.plot((396, 565),(436, 501), marker='o', markerfacecolor='r', label="Ending Coordinates", color='blue')
#plt.legend()
#plt.imshow(blend_image)
#plt.imshow(blend_image)
#plt.show()"""

cap = cv2.VideoCapture("Sample_Video.mp4")
#print("Left Line Starting Coordinates:")
#print(" X ", " Y ")
while(cap.isOpened()):
    _, frame = cap.read()
    canny_image = canny1(frame)
    cropped_image = region_of_interest(canny)
    hough_lines = cv2.HoughLinesP(cropped_image, 2, np.pi / 180, 100, np.array([]), minLineLength=40, maxLineGap=5)
    averaged_lines = average_slope_intercepts(frame, hough_lines)
    line_image = display_lines(frame, averaged_lines)
    blend_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
    cv2.imshow("result", blend_image)

    print(" ")
    print("Hough lines")
    print(hough_lines)
    #print("Left Line  : ", averaged_lines[0])
    #print(averaged_lines[0][0], averaged_lines[0][1])r
    #print("Right Line :", averaged_lines[1])
    if cv2.waitKey(1) == ord("q"):
        break
plt.imshow(blend_image)
plt.show()
cap.release()
cv2.destroyAllWindows()
