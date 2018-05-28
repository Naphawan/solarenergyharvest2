import RPi.GPIO as gpio
import time
import Adafruit_ADS1x15
import pymysql.cursors
from datetime import datetime

class l298n:
	def __init__(self,_ena,_l1,_l2):
		self.l = [_l1,_l2,_ena]
		
		gpio.setmode(gpio.BCM)
		for pin in self.l:
			gpio.setup(pin, gpio.OUT)
		self.pwm = [_ena]
		self.p = []
		for pin in self.pwm:
			p = gpio.PWM(pin,50)
			self.p.append(p)
			p.start(50)

	def drive(self,motor,direction,dc):
		mnum = motor*1
		gpio.output(self.l[mnum], direction)
		gpio.output(self.l[mnum+1], 1-direction)
		# print(self.p[motor])
		self.p[motor].ChangeDutyCycle(dc)

class modestate:
	def __init__(self):
		gpio.setmode(gpio.BCM)
		gpio.setup(5,gpio.OUT)
		gpio.setup(6,gpio.OUT)
		gpio.setup(13,gpio.OUT)
		gpio.setup(19,gpio.OUT)
		gpio.setup(26,gpio.OUT)

	def charging(self):
		gpio.output(5,gpio.HIGH)
		gpio.output(6,gpio.HIGH)
		gpio.output(13,gpio.HIGH)
		gpio.output(19,gpio.LOW)
		gpio.output(26,gpio.LOW)
		# print("Charging")
	def lightactivated(self):
		gpio.output(5,gpio.LOW)
		gpio.output(6,gpio.LOW)
		gpio.output(13,gpio.LOW)
		gpio.output(19,gpio.HIGH)
		gpio.output(26,gpio.HIGH)
		# print("Lighting")

class sun_tracking:
	def __init__(self, ADC,drive):
		self.ADC = ADC
		self.drive_motor = drive

		gpio.setup(20,gpio.IN) #front limit switch
		gpio.setup(21,gpio.IN) #back limit switch

	def track(self,daynight):
		self.e = self.ADC.read_adc(0,2/3)	#Voltage
		self.d = self.ADC.read_adc(1,2/3)	#Current
		self.a = self.ADC.read_adc(2)	#Left LDR
		self.b = self.ADC.read_adc(3)	#Right LDR
		self.c = self.a-self.b
		self.voltage = (self.e/333.0)*(37500.0/7500)
		self.current = (((self.d/333.0)-2.5)/0.185)*1000
		# print(str(self.e) +" "+str(self.d) +" "+str(self.a) +" "+ str(self.b) + " " +str(self.c))
		kP = 0.1

		if daynight:
			if not self.c==0:
					print("c value {}".format(self.c))
					print("Voltage value {:.3f}".format(self.voltage))
					print("Current value {:.3f}".format(self.current))
					if self.c<0:
						if gpio.input(20):
							self.drive_motor.drive(0,0,0)

						else:
							if (self.c>-150):
								self.drive_motor.drive(0,0,0)
								# print("go")
							else:
								self.drive_motor.drive(0,0,15)

					else:
						print(">0")
						if gpio.input(21):
							self.drive_motor.drive(0,1,0)

						else:
							if (self.c<150):
								self.drive_motor.drive(0,1,0)
								# print("go")
							else:
								self.drive_motor.drive(0,1,15)

			# self.drive_motor.drive(0,(abs(self.c)+self.c)/(2*abs(self.c)),abs(self.c)/10)  #50 after

if __name__ == "__main__":
	# Connect to the database
	connection = pymysql.connect(host='192.168.1.45',
								user='faii',
								password='amfaii.',
								db='db_development',
								charset='utf8mb4',
								port=3306,
								cursorclass=pymysql.cursors.DictCursor)
	drive = l298n(23,27,22)
	sun_track = sun_tracking(Adafruit_ADS1x15.ADS1015(),drive)
	modecontroller = modestate()

	gpio.setup(20,gpio.IN)
	gpio.setup(21,gpio.IN)
	
	try:
		t=time.time()
		while 1:
			int(datetime.now().strftime("%H%M"))
			date = int(datetime.now().strftime("%H%M"))		#Time in int ex 00:17 = 17 18:30 = 1830
			print("input 20 {}".format(gpio.input(20)))
			print("inout 21 {}".format(gpio.input(21)))
			# print(date)  


			if (date>600) and (date<1800):      #day
				print("Charging now!!!!!!!!")
				modecontroller.charging()
				sun_track.track(1)
				
				
				
			else:                               #night
				print("light active now!!!!!!!!")
				gpio.output(27,0)
				gpio.output(22,0)
				modecontroller.lightactivated()
				sun_track.track(0)
				
				
						
			if time.time()-t>1:
				#run your task here
				with connection.cursor() as cursor:
					# Create a new record
					sql = "INSERT INTO apps (`created_at`,`updated_at`,`Voltage`,`Current`) VALUES (CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,%s, %s)"
					cursor.execute(sql, (sun_track.voltage, sun_track.current))
					connection.commit()
				t=time.time()
				
	finally:
		# connection.close()
		gpio.cleanup()