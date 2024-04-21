import cv2
import pytesseract
import requests
import time
import os

try:
    import Image
except ImportError:
    from PIL import Image

# Set the current working directory to the directory of the script
current_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_directory)

#============TimeGet==================#
st = time.time()

from datetime import datetime
from datetime import date
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
today = date.today()
date_str = today.strftime("%d/%m/%y")

#================PyTesseract===============#
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe" # Make sure Tessaract is installed in this directory.
face_cascade = cv2.CascadeClassifier('cascade.xml')

img_path = 'images/car.jpg' 
img = cv2.imread(img_path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.01, 7)
for (x, y, w, h) in faces:
    img = cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    cv2.imshow('The car', img)
    area = (x, y, x+w, y+h)

crop_img = img[y:y+h, x:x+w]
gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

(thresh, bw) = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

cv2.imshow("The Plate", bw)

cv2.moveWindow("The car", 540, 120)
cv2.moveWindow("The Plate", 540, 620) # This will change as per the resolution of the camera/image later. 

cv2.imwrite('images/masked_img.jpg', bw)  

img1 = cv2.imread('images/masked_img.jpg')
license_plate = pytesseract.image_to_string(Image.open('images/masked_img.jpg'))

# using isalnum() to filter alphanumeric characters
license_plate_filtered = ''.join(char for char in license_plate if char.isalnum())[:10]

# printing original string
print("Original License Plate: " + license_plate)

# printing license plate after removing non-alphanumeric characters
print("License Plate after removing non-alphanumeric chars: " + license_plate_filtered)

import mysql.connector
mydb = mysql.connector.connect(host="localhost", user="root", passwd="root", database="car")

# ============================Balance reduction=====================#
mycursor = mydb.cursor()

sql = "UPDATE plate SET balance = balance-50 WHERE number = %s"
val = (license_plate_filtered,)

mycursor.execute(sql, val)

# ===================Phone number taken==============================#
sql1 = "SELECT phno FROM plate WHERE number = %s"
val1 = (license_plate_filtered,)

mycursor.execute(sql1, val1)

myresult = mycursor.fetchone()

if myresult is not None:
    for row in myresult:
        print("The user's phone number is : " + str(row))
else:
    print("No phone number found for the given license plate.")

# ===================Balance selection==============================
sql2 = "SELECT balance FROM plate WHERE number = %s"
val2 = (license_plate_filtered,)

mycursor.execute(sql2, val2)
myresult = mycursor.fetchone()

if myresult is not None:
    for bal in myresult:
        print('Your current balance is ' + str(bal))
else:
    print("No balance found for the given license plate.")
mydb.commit()

# =====================The Message==================================

msg1 = 'Your car with ' + license_plate_filtered
msg2 = ' has passed through AEC Toll Booth at ' + str(current_time)
msg3 = ' hrs on ' + date_str
msg4 = '. Your current balance : Rs.' + str(bal) if myresult is not None else ''

msg = msg1 + msg2 + msg3 + msg4

print('The following SMS has been sent. ' + msg)

print('Note : The SMS service in this code has been deprecated and is no longer functional')
# # =====================SMS SERVICE (DEPRECATED NOW)==================================
# URL = 'https://www.sms4india.com/api/v1/sendCampaign'

# # get request
# def sendPostRequest(reqUrl, apiKey, secretKey, useType, phoneNo, senderId, textMessage):
#     req_params = {
#         'apikey': apiKey,
#         'secret': secretKey,
#         'usetype': useType,
#         'phone': phoneNo,
#         'message': textMessage,
#         'senderid': senderId
#     }
#     return requests.post(reqUrl, req_params)

# # get response
# response = sendPostRequest(URL, 'AXCFGC5C0RWX0Q0IC7JXFFTXIE6Q0RTD', 'ROKDZQ3WUN48HVRP', 'stage', row,
#                             'hirakjyotib13@gmail.com', msg)

print("Number plate scanned and debited in : ", time.time() - st, " seconds")
cv2.waitKey(0)
cv2.destroyAllWindows()
