import serial, time
import csv
import psutil as ps
from datetime import datetime
#import lcdLibrary as lcd
from Adafruit_IO import Client
import RPi.GPIO as GPIO
import ADC0834

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

#BtnPin = 16

LedPin = 22
slidePin = 12

#ledPins = [35, 33, 37, 31, 38, 40, 22, 3, 5, 24]
ledPins = [19, 13, 26, 6, 20, 21, 25, 2, 3, 8]
ser = serial.Serial('/dev/ttyUSB0')

x = 0
j = 0
# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_bus=4)

# Initialize library.
disp.begin()

# Get drawing object to draw on image.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)

# Clear display.
draw.rectangle((0,0,width,height), outline = 0, fill = 0)
disp.display()

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
a = 0
# Load default font.
# font = ImageFont.load_default()

#font = ImageFont.truetype('PixelOperatorSC-Bold.ttf', 12)
font = ImageFont.truetype('PixelOperator.ttf', 20)


# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

def setup():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)        # Numbers GPIOs by physical location
	GPIO.setup(slidePin, GPIO.IN)
#	GPIO.setup(BtnPin, GPIO.IN)
	for i in ledPins:
		GPIO.setup(i, GPIO.OUT)   # Set all ledPins' mode is output
		GPIO.output(i, GPIO.HIGH) # Set all ledPins to high(+3.3V) to $
	global led_val
        # Set all LedPin's mode to output and initial level to High(3.3v)
	GPIO.setup(LedPin, GPIO.OUT, initial=GPIO.HIGH)
	ADC0834.setup()
	# Set led as pwm channel and frequece to 2KHz
	led_val = GPIO.PWM(LedPin, 50)
	# Set all begin with value 0
	led_val.start(0)

def main():
	global logger
	logger = Logger()
	global x
	global j
	GPIO.output(LedPin, GPIO.LOW)
#	led_val.ChangeDutyCycle(0)
	while GPIO.input(slidePin) == 1:
		data = []
		for index in range(0,10):
			datum = ser.read()
			data.append(datum)
		pmtwofive = int.from_bytes(b''.join(data[2:4]), byteorder='little') / 10
		x = 0
		for i in range(1):

			if pmtwofive <= 30 and GPIO.input(slidePin) == 1:
				draw.rectangle((0,0,width,height), outline = 0, fill = 0)
				disp.display()
				j = 0
				for pin in ledPins:
					GPIO.output(pin, GPIO.HIGH)
				GPIO.output(ledPins[j], GPIO.LOW)
				draw.rectangle((0,0,width,height), outline = 0, fill = 0)
				while pmtwofive <= 30 and GPIO.input(slidePin) == 1:
					data = []
					for index in range(0,10):
						datum = ser.read()
						data.append(datum)
					pmtwofive = int.from_bytes(b''.join(data[2:4]), byteorder='little') / 10
#					lcd.write(0,0,"AQI:   Great   ")
#					lcd.write(0,1,"PM2.5: " + str(pmtwofive))
					draw.text((x+25, top), "Air Quality",  font=font, fill=255)
					draw.text((x, top+25), "AQI:   Great ",  font=font, fill=255)
					draw.text((x, top+45), "PM2.5:   " + str(pmtwofive),  font=font, fill=255)
					# Display image.
					disp.image(image)
					disp.display()
					draw.rectangle((0,0,width,height), outline = 0, fill = 0)
					disp.display()

			if pmtwofive > 30 and pmtwofive <= 60 and GPIO.input(slidePin) == 1:

				draw.rectangle((0,0,width,height), outline = 0, fill = 0)
				disp.display()
				j = 2
				for pin in ledPins:
					GPIO.output(pin, GPIO.HIGH)
				GPIO.output(ledPins[j], GPIO.LOW)
				y = j
				while y > 0:
					y -= 1
					GPIO.output(ledPins[y], GPIO.LOW)
				draw.rectangle((0,0,width,height), outline = 0, fill = 0)
				while pmtwofive > 30 and pmtwofive <= 60 and GPIO.input(slidePin) == 1:
					data = []
					for index in range(0,10):
						datum = ser.read()
						data.append(datum)
					pmtwofive = int.from_bytes(b''.join(data[2:4]), byteorder='little') / 10
#					lcd.write(0,0,"AQI: Acceptable ")
#					lcd.write(0,1,"PM2.5: " + str(pmtwofive))
					draw.text((x+25, top), "Air Quality",  font=font, fill=255)
					draw.text((x, top+25), "AQI:   Acceptable",  font=font, fill=255)
					draw.text((x, top+45), "PM2.5:   " + str(pmtwofive),  font=font, fill=255)
					# Display image.
					disp.image(image)
					disp.display()

					draw.rectangle((0,0,width,height), outline = 0, fill = 0)
					disp.display()
					
			if pmtwofive > 60 and pmtwofive <= 90 and GPIO.input(slidePin) == 1:
				
				draw.rectangle((0,0,width,height), outline = 0, fill = 0)
				disp.display()
				j = 3
				for pin in ledPins:
					GPIO.output(pin, GPIO.HIGH)
				GPIO.output(ledPins[j], GPIO.LOW)
				y = j
				while y > 0:
					y -= 1
					GPIO.output(ledPins[y], GPIO.LOW)
				draw.rectangle((0,0,width,height), outline = 0, fill = 0)
				while pmtwofive > 60 and pmtwofive <= 90 and GPIO.input(slidePin) == 1:
					data = []
					for index in range(0,10):
						datum = ser.read()
						data.append(datum)
					pmtwofive = int.from_bytes(b''.join(data[2:4]), byteorder='little') / 10
#					lcd.write(0,0,"AQI:    Fair    ")
#					lcd.write(0,1,"PM2.5: " + str(pmtwofive)
					draw.text((x+25, top), "Air Quality",  font=font, fill=255)
					draw.text((x, top+25), "AQI:   Fair ",  font=font, fill=255)
					draw.text((x, top+45), "PM2.5:   " + str(pmtwofive),  font=font, fill=255)
					# Display image.
					disp.image(image)
					disp.display()

					draw.rectangle((0,0,width,height), outline = 0, fill = 0)
					disp.display()
					
			if pmtwofive > 90 and pmtwofive <= 120 and GPIO.input(slidePin) == 1:
				
				draw.rectangle((0,0,width,height), outline = 0, fill = 0)
				disp.display()
				j = 5
				for pin in ledPins:
					GPIO.output(pin, GPIO.HIGH)
				GPIO.output(ledPins[j], GPIO.LOW)
				y = j
				while y > 0:
					y -= 1
					GPIO.output(ledPins[y], GPIO.LOW)
				draw.rectangle((0,0,width,height), outline = 0, fill = 0)
				while pmtwofive > 90 and pmtwofive <= 120 and GPIO.input(slidePin) == 1:
					data = []
					for index in range(0,10):
						datum = ser.read()
						data.append(datum)
					pmtwofive = int.from_bytes(b''.join(data[2:4]), byteorder='little') / 10
#					lcd.write(0,0,"AQI:    Poor    ")
#					lcd.write(0,1,"PM2.5: " + str(pmtwofive))
					draw.text((x+25, top), "Air Quality",  font=font, fill=255)
					draw.text((x, top+25), "AQI:   Poor ",  font=font, fill=255)
					draw.text((x, top+45), "PM2.5:   " + str(pmtwofive),  font=font, fill=255)
					# Display image.
					disp.image(image)
					disp.display()

					draw.rectangle((0,0,width,height), outline = 0, fill = 0)
					disp.display()
					
			if pmtwofive > 120 and pmtwofive <= 150 and GPIO.input(slidePin) == 1:
				
				draw.rectangle((0,0,width,height), outline = 0, fill = 0)
				disp.display()

				j = 7
				for pin in ledPins:
					GPIO.output(pin, GPIO.HIGH)
				GPIO.output(ledPins[j], GPIO.LOW)
				y = j
				while y > 0:
					y -= 1
					GPIO.output(ledPins[y], GPIO.LOW)
				while pmtwofive > 120 and pmtwofive <= 150 and GPIO.input(slidePin) == 1:
					data = []
					for index in range(0,10):
						datum = ser.read()
						data.append(datum)
					pmtwofive = int.from_bytes(b''.join(data[2:4]), byteorder='little') / 10
#					lcd.write(0,0,"AQI:    Poor    ")
#					lcd.write(0,1,"PM2.5: " + str(pmtwofive))
					draw.text((x+25, top), "Air Quality",  font=font, fill=255)
					draw.text((x, top+25), "AQI:   Poor",  font=font, fill=255)
					draw.text((x, top+45), "PM2.5:   " + str(pmtwofive),  font=font, fill=255)
					# Display image.
					disp.image(image)
					disp.display()

					draw.rectangle((0,0,width,height), outline = 0, fill = 0)
					disp.display()
					
			if pmtwofive > 150 and pmtwofive <= 210 and GPIO.input(slidePin) == 1:
				
				draw.rectangle((0,0,width,height), outline = 0, fill = 0)
				disp.display()
				j = 8
				for pin in ledPins:
					GPIO.output(pin, GPIO.HIGH)
				GPIO.output(ledPins[j], GPIO.LOW)
				y = j
				while y > 0:
					y -= 1
					GPIO.output(ledPins[y], GPIO.LOW)
				while pmtwofive > 150 and pmtwofive <= 210 and GPIO.input(slidePin) == 1:
					data = []
					for index in range(0,10):
						datum = ser.read()
						data.append(datum)
					pmtwofive = int.from_bytes(b''.join(data[2:4]), byteorder='little') / 10
#					lcd.write(0,0,"AQI:  Very Poor ")
#					lcd.write(0,1,"PM2.5: " + str(pmtwofive))
					draw.text((x+25, top), "Air Quality",  font=font, fill=255)
					draw.text((x, top+25), "AQI:   Very Poor ",  font=font, fill=255)
					draw.text((x, top+45), "PM2.5:   " + str(pmtwofive),  font=font, fill=255)
					# Display image.
					disp.image(image)
					disp.display()
					
					draw.rectangle((0,0,width,height), outline = 0, fill = 0)
					disp.display()
					
			if pmtwofive > 210 and GPIO.input(slidePin) == 1:
					
				draw.rectangle((0,0,width,height), outline = 0, fill = 0)
				disp.display()
				j = 9
				for pin in ledPins:
					GPIO.output(pin, GPIO.HIGH)
				GPIO.output(ledPins[j], GPIO.LOW)
				y = j
				while y > 0:
					y -= 1
					GPIO.output(ledPins[y], GPIO.LOW)
				while pmtwofive > 210 and GPIO.input(slidePin) == 1:
					data = []
					for index in range(0,10):
						datum = ser.read()
						data.append(datum)
					pmtwofive = int.from_bytes(b''.join(data[2:4]), byteorder='little') / 10
#					lcd.write(0,0,"AQI:  Severe ")
#					lcd.write(0,1,"PM2.5: " + str(pmtwofive))
					draw.text((x+25, top), "Air Quality",  font=font, fill=255)
					draw.text((x, top+25), "AQI:   Severe",  font=font, fill=255)
					draw.text((x, top+45), "PM2.5:   " + str(pmtwofive),  font=font, fill=255)
					# Display image.
					disp.image(image)
					disp.display()
					
					draw.rectangle((0,0,width,height), outline = 0, fill = 0)
					disp.display()
					

			x += 30
			j = 0

def photoresistor():
	global logger
	logger = Logger()
	for i in ledPins:
		GPIO.output(i, GPIO.HIGH)
	while GPIO.input(slidePin) == 0:
#		GPIO.output(LedPin, GPIO.HIGH)
		led_val.ChangeDutyCycle(100)
		draw.rectangle((0,0,width,height), outline = 0, fill = 0)
		disp.display()
		analogVal = ADC0834.getResult()
#		print ('analog value = %d' % analogVal)
		if (analogVal <= 65):
			quality = "Clean"
		elif (analogVal > 65 and analogVal <= 72):
			quality = "Usable"
		elif (analogVal > 72 and analogVal <= 87):
			quality = "Cloudy"
		elif (analogVal > 87 and analogVal <= 99):
			quality = "Murky"
		elif (analogVal > 99):
			quality = "Dirty"

		draw.text((a+18, top), "Water Quality",  font=font, fill=255)
		draw.text((a, top+20), "Value:  %d" % analogVal,  font=font, fill=255)
		draw.text((a, top+40), "Quality:   " +  quality, font = font, fill = 255)
		# Display image
		disp.image(image)
		disp.display()
#		led_val.ChangeDutyCycle(analogVallue*100/255)

class Logger:
    def __init__(self):
        self.data_dict = {}

    def collect_data1(self, pmtwofive):
        self.data_dict['aqi'] = ("Time: " + str(datetime.now()) + " ", "  PM2.5: " + str(pmtwofive))
        
    def collect_data2(self, analogVal):
        self.data_dict['water'] = ("Time: " + str(datetime.now()) + " ", "  PM2.5: " + str(analogVal))

    def log_data(self):
        for file, data in self.data_dict.items():
            with open('data/' + file + '.csv', 'a+', newline = '') as f:
                writer = csv.writer(f)
                writer.writerow(data)


def destroy():
	draw.rectangle((0,0,width,height), outline = 0, fill = 0)
	disp.image(image)
	disp.display()
	GPIO.output(LedPin, GPIO.HIGH)
	for pin in ledPins:
		GPIO.output(pin, GPIO.LOW)    # turn off all leds
	led_val.stop()
	GPIO.cleanup()

if __name__ == "__main__":
	setup()
	try:
		while True:
			if GPIO.input(slidePin) == 1:
				led_val.ChangeDutyCycle(0)
				print("Program Running: Air Quality Monitor")
				main()
			elif GPIO.input(slidePin) == 0:
				print("Program Running: Water Quality Monitor")
				photoresistor()
	except KeyboardInterrupt:
		destroy()


