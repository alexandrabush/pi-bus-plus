from pghbustime import *
from collections import OrderedDict
from datetime import datetime, date, time
import math
import Adafruit_CharLCD as LCD
import RPi.GPIO as GPIO

#button setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.IN,pull_up_down=GPIO.PUD_UP)

#lcd setup
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

#setup
mykey = "KK6JMVmf2H3wSjkHXZ877bXWm"
api = BustimeAPI(mykey)

#stops
murrayID = 7096
starbucksID = 7233
mArrival = "N\A"
mBus = "N\A"
sArrival = "N\A"
sBus = "N\A"

while True:
	buttonState = GPIO.input(12)
	if buttonState == False:
		print "button pressed"
		#get murray stop info
		mydict = api.predictions(murrayID, maxpredictions=1)
		info = mydict["prd"]

		for k,v in info.items():
			#prdtm is the predicted arrival time
			if "prdtm" == k:
				mArrival = v
			#rt is the bus 
			if "rt" == k:
				mBus = v


		#get shady stop info
		mydict = api.predictions(starbucksID, maxpredictions=1)
		info = mydict["prd"]

		for k,v in info.items():
			if "prdtm" == k:
				sArrival = v
			if "rt" == k:
				sBus = v

		# get current time 
		cTime = datetime.now().time()

		# convert times and calc # of minutes until arrival
		mArrival = datetime.strptime(mArrival, "%Y%m%d %H:%M:%S")
		sArrival = datetime.strptime(sArrival, "%Y%m%d %H:%M:%S")

		sminutes = datetime.combine(date.today(), sArrival.time()) - datetime.combine(date.today(), cTime)
		sminutes = math.floor(sminutes.total_seconds()/60)
		sminutes = math.trunc(sminutes)

		mminutes = datetime.combine(date.today(), mArrival.time()) - datetime.combine(date.today(), cTime)
		mminutes = math.floor(mminutes.total_seconds()/60)
		mminutes = math.trunc(mminutes)

		#print data to lcd
		lcd.set_cursor(0,0)
		lcd.message("Murray: "+ mBus + "  " + str(mminutes) + "m")
		lcd.set_cursor(0,1)
		lcd.message("Shady:  "+ sBus + "  " + str(sminutes) + "m")


