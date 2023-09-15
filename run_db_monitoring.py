import time
import datetime
import sched
import pigpio

def main():

	#Entering main script
	print("Starting up")


	#Enable reading of bus and create handle
	pi = pigpio.pi()
	h = pi.i2c_open(1, 0x48) #open device at address 0x48 on bus 1
	#Try a first read
	first_db = pi.i2c_read_byte_data(h, 0x0A)
	print ("First db is" + str(first_db))


	#Set up scheduler to read each second
	def read_db(scheduler):
		#schedule the first call
		scheduler.enter(1, 1, read_db, (scheduler,))
		#Execute the sound buffer reads
		db = pi.i2c_read_byte_data(h, 0x0A)
		print ("db is " + str(db) + ' @ ' + str(datetime.datetime.now()))
		return db

	#Execute/schedule 1 second sound readings
	scheduled_sound_read=sched.scheduler(time.time, time.sleep)
	scheduled_sound_read.enter(1, 1, read_db, (scheduled_sound_read,))
	print("Start reading sound levels")
	scheduled_sound_read.run()


if __name__ == "__main__":
	main()
