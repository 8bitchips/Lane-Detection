# Lane-Detection
Lane Detection using Hough Transform and Canny <br> <br>


https://www.youtube.com/watch?v=eLTLtUVuuy4&list=PLerVuzMDG1PlXrcDjGNU8tU_O9dmOW2FM&index=9 <br><br>


<h1> Lane Detection </h1>
Let’s start with colors and they’re channels.
Normal colored images have RGB, that’s why they’re colored. So, in total there are 3 channels R, G, B ranging from (0, 255).

These values from (0, 255) are the array range for each color i.e., 0 for darkest shade and 255 for the brightest shade for each channel.

It’s difficult and time consuming for the computer to compute 3 channels that’s why we convert images to greyscale, so that we can get the array range in just one channel (easier and faster computational purpose).

<h2> Step 1: Edge Detection </h2>

![image](https://user-images.githubusercontent.com/87309254/179006085-614f3efe-24f4-4e87-a116-10c720e086c9.png)

<h3> An image can be written as a matrix i.e., an array of pixels <h3>

![image](https://user-images.githubusercontent.com/87309254/179006163-9750ec7a-af0c-4976-a4b3-8ac3e2a91052.png)

<br> Gradient: Measure of change or brightness over adjacent pixel. <br>

<h3> Strong Gradient : <br>
Strong Gradient represents a sharp change  </h3>

![image](https://user-images.githubusercontent.com/87309254/179006608-b8edbd04-25b9-4afd-814c-6269f2f45800.png) <br>

<h3> Weak Gradient : <br>
Shallow gradient represents a shallow change. </h3> 

![image](https://user-images.githubusercontent.com/87309254/179006655-a915e15b-2aec-425f-aaeb-713b4ee8dc96.png) <br> 


<h2 >Example </h2>

![image](https://user-images.githubusercontent.com/87309254/179006693-1b782ad4-9873-4905-bdde-fbecd7084890.png)

<h3> To convert image from RGB to Grayscale using CV2: <br>
var1 = cv2.cvtCOLOR(img_name, cv2.COLOR_RGB2GRAY) </h3> <br> <br>


<h2> Step 2: Reduce Noise and Smoothen Image </h2>

Read Kernel Convolution 

<b> Gaussian Blur Smoothens the image to reduce noise as that could misinterpret the edges.
It takes the weights of all the pixels around each pixel and creates a new image with weighted distribution. </b>

blur = cv2.GaussianBlur(gray, (5, 5), 0) <br>
<h3> So here we’re applying Gaussian Blur to an image with a 5 by 5 Kernel and Standard Deviation as 0. </h3>

<h3> Read about Canny() function. (It automatically applies a 5x5 Gaussian Blur to the image when called) </h3>

![image](https://user-images.githubusercontent.com/87309254/179008948-80e97400-9b2f-40b1-8e42-254d9148035c.png)
 
See in the above picture, the leftmost pic has lot of noise but the noise reduces as we move to the right, this is because of the Gaussian Blur! <br> <br>


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

![image](https://user-images.githubusercontent.com/87309254/179012303-bd7d0484-c61a-406d-abb8-88be7b824447.png)
![image](https://user-images.githubusercontent.com/87309254/179012322-c84e2c77-15c6-4eb7-b5c9-41bdaf9c3f9c.png)  

<br>
<br>
 
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

![image](https://user-images.githubusercontent.com/87309254/179014483-d6ec76eb-6e90-480f-b9a4-f1dbf42c6571.png)


