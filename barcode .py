import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2
import sys
#_________________________________________________DATABASE OPENED AND DATA EXTRACTION____________________________________________
def info(idno):
	import psycopg2
	print(str(int(idno)))
	conn = psycopg2.connect(database = "barcode", user = "myuser", password = "mypass", host = "127.0.0.1", port = "5432")

	cur = conn.cursor()
	print(type(str(int(idno))))
	cur.execute("SELECT id,price,weight,name from info1 where id = " + "'" + str(int(idno))  +"'")
	rows = cur.fetchall()
	if len(rows)!=0:
		for row in rows:
			ID = row[0]
			PRICE = row[1]
			WEIGHT = row[2]
			NAME = row[3]
		conn.close()
		spech("id is"+ str(ID) + "product name is"+str(NAME)+"product price is"+str(PRICE)+"Rupees"+"product weight is"+str(WEIGHT)+"Grams")
	else:
		spech("ID IS NOT STORED")
		
	

#___________________________________________IDEXTARACTION_______________________________________________________________________
def decode1(im) : 
	cv2.imshow('frame2',im)
	decodedObjects = pyzbar.decode(im)
	if decodedObjects == []:
		speech("sorry barcode is not detected please try again")

	else: 
		for obj in decodedObjects:
			print('Type : ', obj.type)
			print('Data : ', obj.data,'\n')
			info(obj.data)
		
	return decodedObjects

#_____________________________________________________READING OF BARCODE_________________________________________________________
def decode(im) : 
	#cv2.imshow('frame1',im)
	decodedObjects = pyzbar.decode(im)
	if decodedObjects == []:
		return True

	else: 
		return False

#_______________________________________________________TEXT TO SPEECH___________________________________________________________
def spech(mytext):
	# Import the required module for text  
	# to speech conversion 
	from gtts import gTTS 
  
	# This module is imported so that we can  
	# play the converted audio 
	import os 
  
	# The text that you want to convert to audio 
	t = mytext
	  
	# Language in which you want to convert 
	language = 'en'
  
	# Passing the text and language to the engine,  
	# here we have marked slow=False. Which tells  
	# the module that the converted audio should  
	# have a high speed 
	myobj = gTTS(text=t, lang=language, slow=False) 
	  
	# Saving the converted audio in a mp3 file named 
	# welcome  
	myobj.save("welcome.mp3") 
	  
	# Playing the converted file 
	os.system("mpg321 welcome.mp3") 


#________________________________________________________BEEP SYSTEM_____________________________________________________________
def beep(frame,i,maxx):
	import cv2
	import numpy as np
	import os
	import argparse
	import imutils
	
	try:
		k=1
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		ddepth = cv2.cv.CV_32F if imutils.is_cv2() else cv2.CV_32F
		gradX = cv2.Sobel(gray, ddepth=ddepth, dx=1, dy=0, ksize=-1)
		gradY = cv2.Sobel(gray, ddepth=ddepth, dx=0, dy=1, ksize=-1)

		gradient = cv2.subtract(gradX, gradY)
		gradient = cv2.convertScaleAbs(gradient)

		blurred = cv2.blur(gradient, (9, 9))
		(_, thresh) = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY)

		kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
		closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
		closed = cv2.erode(closed, None, iterations = 4)
		closed = cv2.dilate(closed, None, iterations = 4)



		cnts = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)
		c = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
		print(c)
		area = max(sum(sum(c)))
		print(area)
		if(area > maxx):
			maxx = area
			if(i<3000):
				i=i+100
		else:
			i=i-1000
		return i
	
	except IndexError:
		#print("continue")	
		return 0




#_____________________________________________________________IMAGE OR VIDEO RETRIVAL____________________________________________
def camera():
	maxx=0
	i=100
	import cv2
	import numpy as np
	import os
 
	cap = cv2.VideoCapture(0)
 
	if (cap.isOpened() == False): 
		print("Unable to read camera feed")
 
	# Default resolutions of the frame are obtained.
	frame_width = int(cap.get(3))
	frame_height = int(cap.get(4))
	k=0
	check = True
	count=0
	while(check):
		ret, frame = cap.read()
		if ret == True: 
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			check = decode(gray)
			i=beep(frame,i,maxx)

			os.system('play -n synth 0.1 sine {} vol 0.2'.format(i))
			cv2.imshow('frame',frame)
			if check == False:
			# Display the resulting frame    
				cv2.imshow('frame',frame)
				decode1(gray)
			# Press Q on keyboard to stop recording
			if cv2.waitKey(1) & 0xFF == ord('q'):
			      break 
	  	# Break the loop
		else:
			break 
	 
	cap.release()
	cv2.destroyAllWindows()	

#______________________________________________________MAIN FUNCTION_____________________________________________________________
if __name__ == '__main__':


	spech("please try to locate your product barcode on the upper side")
	frame = camera()


