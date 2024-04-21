# Smart_TollBooth_System
The project aims to implement an automated prepaid toll system with vehicle recognition and notification features to streamline toll collection, minimize traffic congestion, and enhance efficiency while reducing paperwork and promoting environmental sustainability.

Contents:
Images - This folder requires a frontal picture of a car with a license plate visible. Filename should be "car.jpg"
cascade.xml - This was the output of our training using TensorFlow and a Nvidia GPU over a few hundred Indian Vehicles. 
final.py - This is the file to execute with python. It will read the "car.jpg" file, mask out the license plate and run PyTesseract OCR on it. 
Run.bat - This is just a helper batch file to run on Windows machines with ease.
