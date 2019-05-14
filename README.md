# Overview
To help people live a healthier life and reduce waste of fruits, we propose a smart refrigerator system with corresponding application to keep track of fruits’ expired date and users’ nutrition intake. The main challenge is fruit recognition where we used Convolution Neural Networks (CNNs) to have trained a model with 97.6% accuracy. And we have accomplished our goal of recognition, alert, recommendation and android application. 


# Functions
1. Take picture and do recognition.

2. Alter user when the fruits in the refrigerator are about to be out of date.

3. Keep track of what user put into the refrigerator and what they have eaten.

4. Recommend fruits to user based on the amount of vitamin they have taken.

# FileSystem
android: andriod app, to interact with end users 

classifcation_alert: program to do classification and alert users 

models: machine learning model to do fruit classification

raspberrryPi: get the weight and take picture of the fruit, and upload the information to database

server: andriod app server
