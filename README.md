# Lane-Detection
Lane Detection using Hough Transform and Canny <br> <br>


https://www.youtube.com/watch?v=eLTLtUVuuy4&list=PLerVuzMDG1PlXrcDjGNU8tU_O9dmOW2FM&index=9 <br><br>


<h1> Lane Detection </h1>
Let’s start with colors and they’re channels.
Normal colored images have RGB, that’s why they’re colored. So, in total there are 3 channels R, G, B ranging from (0, 255).

These values from (0, 255) are the array range for each color i.e., 0 for darkest shade and 255 for the brightest shade for each channel.

It’s difficult and time consuming for the computer to compute 3 channels that’s why we convert images to greyscale, so that we can get the array range in just one channel (easier and faster computational purpose).

<b> ------------------------------------------------------------------------------------------------------------------------------------------------------------- </b>
 
<br>

<h2> Step 1: Edge Detection </h2>

![image](https://user-images.githubusercontent.com/87309254/179006085-614f3efe-24f4-4e87-a116-10c720e086c9.png)

<h3> An image can be written as a matrix i.e., an array of pixels <h3>

![image](https://user-images.githubusercontent.com/87309254/179006163-9750ec7a-af0c-4976-a4b3-8ac3e2a91052.png)
 
<br> Gradient: Measure of change or brightness over adjacent pixel. <br>

Strong Gradient                                                   |                              Weak Gradient 
:----------------------------------------------------------------:|:-------------------------------------------------------------: 
Strong Gradient represents a sharp change                         |      Shallow gradient represents a shallow change.
![image](https://user-images.githubusercontent.com/87309254/179006608-b8edbd04-25b9-4afd-814c-6269f2f45800.png) | ![image](https://user-images.githubusercontent.com/87309254/179006655-a915e15b-2aec-425f-aaeb-713b4ee8dc96.png)
 
<h2 >Example </h2>

![image](https://user-images.githubusercontent.com/87309254/179006693-1b782ad4-9873-4905-bdde-fbecd7084890.png)

<h3> To convert image from RGB to Grayscale using CV2: <br>
var1 = cv2.cvtCOLOR(img_name, cv2.COLOR_RGB2GRAY) </h3> <br> <br>

<b> ------------------------------------------------------------------------------------------------------------------------------------------------------------- </b>
 
<br>
 
<h2> Step 2: Reduce Noise and Smoothen Image </h2>

Read Kernel Convolution 

<b> Gaussian Blur Smoothens the image to reduce noise as that could misinterpret the edges.
It takes the weights of all the pixels around each pixel and creates a new image with weighted distribution. </b>

blur = cv2.GaussianBlur(gray, (5, 5), 0) <br>
<h3> So here we’re applying Gaussian Blur to an image with a 5 by 5 Kernel and Standard Deviation as 0. </h3>

<h3> Read about Canny() function. (It automatically applies a 5x5 Gaussian Blur to the image when called) </h3>

![image](https://user-images.githubusercontent.com/87309254/179008948-80e97400-9b2f-40b1-8e42-254d9148035c.png)
 
See in the above picture, the leftmost pic has lot of noise but the noise reduces as we move to the right, this is because of the Gaussian Blur! <br> <br>

 <b> ------------------------------------------------------------------------------------------------------------------------------------------------------------- </b>
 
<br>

<br> <h2> Step 3: Finding Lanes Lines - canny() </h2>

![image](https://user-images.githubusercontent.com/87309254/179009680-ed0e9cb1-913a-4a8c-b3f6-eca06c85f02f.png)

<h3 >The whole image is an array of numbers with different intensities.<br>
It can be represented as a big array with, <br>
x as the image width  <br>
y as the image height<br>
Subtract the product of the width and the height we get the total number of pixels in our image. </h3> <br>


This can also be looked not only as an array but also as a function, so since it’s a function, we can apply mathematical operators on them. <br> <br>

For this specific one we will use the Derivative Function. <br>
<b> The canny() function does the same for us. </b> <br>
It calculates the derivative of both the x and y directions thereby measuring the change in intensity with respect to adjacent pixels. <br>

<h3> Small Derivative = Small change in intensity <br>
Big Derivative = Big change in intensity <br>
Hence by doing this we are calculating the Gradient of the Image </h3> <br>



<br> <h3> When we call the canny() function in computes the gradient in all directions of our blurred images and traces the strongest gradient as a series if white pixels. <br> <br>
canny = cv2.Canny(image, low_threshold, high_threshold) </h3> <br>

<h3> 	If the value is higher than the high_threshold then it is accepted as the edge pixel. <br>
	If the value is lower than the low_threshold then it is rejected. <br>
	If the value of the gradient is between the low_threshold and high_threshold it will be accepted only if it is connected to a strong edge. </h3> <br>

The documentation suggests to use a ratio of 1:1 or 1:3 <br>
So here we use 50:150 i.e., 1:3 <br>

<h3> Now to show the image in terms of graph we use matplot.pyplot as plt <br>
plt.imshow(canny) <br>
plt.show() </h3> <br>
 
<p>
<img align="left" src="https://user-images.githubusercontent.com/87309254/179012303-bd7d0484-c61a-406d-abb8-88be7b824447.png" width="400" heigth="150"> 
<img align="bottom" src="https://user-images.githubusercontent.com/87309254/179012322-c84e2c77-15c6-4eb7-b5c9-41bdaf9c3f9c.png" with="150" heigth="150">
</p>
 
<br>
<br>

<b> ------------------------------------------------------------------------------------------------------------------------------------------------------------- </b>
 
<br> <br>
 
<h2> Step 4 : Finding lane Lines - Region of Interest	</h2>

![image](https://user-images.githubusercontent.com/87309254/179013580-dd9611c2-222c-4ac7-867d-4b5037590eaa.png)
 
This is where we calculate on the graph of the image the points where we need to have the lane or the edges.
We give triangular/polygonal coordinates to trace the edges along the road. <br>

<h3> We create a function named region_of_interest(image): <br>
Specify the region of interest dimensions in a polygon variable named triangle,  <br>
height = image.shape[0] <br>
triangle = np.array([[200, height) ,(1100, height), (550, 250)]]) </h3> <br>

Here we are basically creating a black mask to be traced along these coordinates given <br>
mask = np.zeros_like(image) <br>
image can be written as an array of pixels, zeros_like creates an array of zeros with the same shape as the images corresponding array.  Both arrays will therefore have the same number of rows and columns which means the mask will have the same number of pixels and thus the same dimensions as our canny image. The pixels of this mask will be completely black as they have zero intensity. <br>


<h3> Now we have to fill our mask with the polygon coordinates using OpenCV’s fillPoly() function <br>
cv2.fillPoly(mask, triangle, 255) <br>
Mask – Black image with the same dimension <br>
Triangle – region of interest coordinates <br>
255 – color of the region of interest </h3> <br>

<h3> Why did we do all this…? </h3>
We were learning how to mask and poly fill an image, so that we just want to use the edges in the canny i.e., just the part of the lane we want to use rather than the whole picture or road! <br>
So instead of having white all over the black mask we will use the edges of the road withing the polygon coordinates. <br> <br>

![image](https://user-images.githubusercontent.com/87309254/179014483-d6ec76eb-6e90-480f-b9a4-f1dbf42c6571.png) <br> <br>

<b> ------------------------------------------------------------------------------------------------------------------------------------------------------------- </b>

<h1> Bitwise AND </h1>
 
As we discussed earlier, an image is an array of integers. <br>
The masked image is a complete black image with white color in the polygon specified <br>
 
<h3> Black has no intensity so it’s 0 and white has max intensity so it’s 1. <br>
In the other main image [canny()], we have the complete image blacked out and only the edges white and once again here black = 0 and white = 1 </h3> <br>

Here we will combine both the images by using bitwise AND operation!!!
<h3> Bitwise AND <br>
0 & 0 = 0 <br>
0 & 1 = 0 <br>
1 & 0 = 0 <br>
1 & 1 = 1 </h3> <br>

So, when we perform bitwise AND on these 2 images wherever there is:
<h3> Black (0) & Black (0) = Black (0) <br>
Black (0) & White (1) = Black (0) <br>
White (1) & Black (0) = Black (0) <br>
White (1) & White (1) = White (1) </h3> <br> 
 
![image](https://user-images.githubusercontent.com/87309254/179017098-ecbd3044-c739-456a-9e66-0283a149b09a.png)  <br> <br>

<h3> What’s the output…? </h3> 
<h4> The whole canny() image gets black except the region of the polygon <br>
So, wherever there was white within the region of the polygon, it has remained white and wherever there was black it has remained as is. </h4> <br>
 
![image](https://user-images.githubusercontent.com/87309254/179017179-3d22f6a9-f430-4617-99f2-3e4f71b455df.png)

<br> <br> <br>
 
<b> ------------------------------------------------------------------------------------------------------------------------------------------------------------- </b>

<br>
 
<h2> Hough_lines = cv2.HoughLinesP(cropped_image, 2, np.pi/180, 85, np.array([]), min_line_lenght=40, max_line_gap=5) </h2> 
 
<h3> 1.	This is the output with 20 pixels as the bit resolution and 5 degrees. </h3>
 
![image](https://user-images.githubusercontent.com/87309254/179023202-1b280d72-3f4d-4357-917f-7d698d673a57.png)

<h3> 2.	This is the output with 2 pixels as the bit resolution and 1 degree </h3>
 
![image](https://user-images.githubusercontent.com/87309254/179023227-88610182-4e0b-4631-9205-625eee72b916.png)


<h3>
2)  The 2nd Parameter ->  2 is the bit resolution in pixels. <br> <br>
3)  The 3rd Parameter ->  np.pi/180 = 1 is the degree. <br> <br>
4)  The 4th parameter is the threshold for the optimal number of increments for the accumulator array cell determination.  <br> <br>
5)  The 5th argument is just a placeholder array, so just create any empty array. <br> <br>
6)  The 6th argument is the minimum line length to be traced. So, if the traced min_line_lenght is less than 40 it will not be accepted as a relevant line. <br> <br>
7)  The 7th argument is the max_line_gap, which is the max line gap between segmented lines to be traced and connected instead of them being broken up. <h3> 

 
<br> <br>
In display_lines function: <br>
The output we get for the lines is a 2D array, but we need is a 1D array <br>
So, we reshape every line into a 1D array by writing line.reshape(4) <br>
 
![image](https://user-images.githubusercontent.com/87309254/179024271-9ff45d89-6c76-4c8c-a45b-6e204a17d89a.png)


cv2.addWeighted(lane_image, 0.8, line_image, 1, 1) <br>
This adds the 2 images given as parameters. <br>  <br>
 
Since the background of the line_image is black i.e., the array is [0] wherever black <br>
And adding 0 to any number is that number itself, so the original image doesn’t get altered at all, except the lines drawn is added.  <br>

 
