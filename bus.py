#-----------------------------------------------------------------------------------------------------------
#
#	Pi Bus Plus
#	Gets next 2 bus ETAs and displays them on a 16x2 LCD
#
#	By Alexandra Bush
#	Last Edited: 11.30.17
#
#-----------------------------------------------------------------------------------------------------------

import math
import Adafruit_CharLCD as LCD
import RPi.GPIO as GPIO
from pghbustime import *
from collections import OrderedDict
from datetime import datetime, date, time

#------------------------------------------------------------------------------------------------------------

def hardwareSetup():

	#Sets up the button
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(12, GPIO.IN,pull_up_down=GPIO.PUD_UP)

	#Sets up the LCD display
	lcd_rs = 25
	lcd_en = 24
	lcd_d4 = 23
	lcd_d5 = 17
	lcd_d6 = 18
	lcd_d7 = 22
	lcd_backlight = 2
	lcd_columns = 16
	lcd_rows = 2

	lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
	lcd.enable_display(True)

	return lcd

#------------------------------------------------------------------------------------------------------------

def getNextBus(stopID, api):
	
	#Get stop info from the API
	mydict = api.predictions(stopID, maxpredictions=1)
	info = mydict["prd"]
	
	#set up vars
	arrival = "n/a"
	bus = "n/a"

	for k,v in info.items():
		#prdtm is the predicted arrival time
		if "prdtm" == k:
			arrival = v
		#rt is the bus 
		if "rt" == k:
			bus = v

	return arrival, bus

#------------------------------------------------------------------------------------------------------------

def calcMinutesToArrival(arrivalTime):

	#get current time
	cTime = datetime.now().time()

	# convert arrival time to the proper format
	arrivalTime = datetime.strptime(arrivalTime, "%Y%m%d %H:%M:%S")

	#calc minutes to arrival
	minutes = datetime.combine(date.today(), arrivalTime.time()) - datetime.combine(date.today(), cTime)
	minutes = math.floor(minutes.total_seconds()/60)
	minutes = math.trunc(minutes)

	return minutes

#------------------------------------------------------------------------------------------------------------

#Init hardware and API key
mykey = "KK6JMVmf2H3wSjkHXZ877bXWm"
api = BustimeAPI(mykey)
lcd = hardwareSetup()

#Init stop IDs
murrayID = 7096
shadyID  = 7233

#Poll button for input; on click, update bus info
while True:
	buttonState = GPIO.input(12)

	if buttonState == False:

		#for debugging
		print "button pressed"

		# get the info on next arrivals
		mArrival, mBus = getNextBus(murrayID, api)
		sArrival, sBus = getNextBus(shadyID, api)

		# calculate minutes until each bus arrives
		mminutes = calcMinutesToArrival(mArrival)
		sminutes = calcMinutesToArrival(sArrival)

		#print bus data to lcd
		lcd.set_cursor(0,0) #first row
		lcd.message("Murray: "+ mBus + "  " + str(mminutes) + "m")
		lcd.set_cursor(0,1) #second row
		lcd.message("Shady:  "+ sBus + "  " + str(sminutes) + "m")
