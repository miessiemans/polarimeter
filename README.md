# polarimeter
Using colour comparison to increase accuracy of Polarimeter


Part of a project I did at University to extend an experiment investigating the photoactivity of sugar solutions. 
The code takes a feed using any webcam using the OpenCV library and compares a 10x10 grid of pixels around 2 chosen points and compares them in LAB colourspace using a Euclidean distance; when a threshold is triggered it will read "aligned" while also showing a visual cue for how close the two colours are, if the camera needs to be adjusted press "c" and the calibration screen will come up and you can pick 2 new points. 

Ensure the focus doesn't change too much, so either turn off autofocus or use a darker environment for the experiment. 


A polarimeter is an instrument used in every UG-Lab which analyses the angle of polarity of light after it passes through a sample against the reflected light before it interacts with a sample, so when the brightness of the light through an analyser polarising lens we can see at what angle the light is polarised compared to the original polarity. 
This is useful in Physics and Chemistry, and using this elementary code you can increase the accuracy as the Polarimeter has a resolution to 0.01 degree, but with the human eye the colour / brightness is pretty indistinguishable for a range (for me at least) of 5 degrees. 
So I thought I'd put the code here for anyone to use with a webcam!

I used my iPhone, using an app called IVCam, any IPCam or video feed to your laptop would work
Just a UG Physics student uploading some code someone might find useful! 
