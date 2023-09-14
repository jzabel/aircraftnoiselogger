import time
import sched
import pigpio

def main():

	#Entering main script

	#Enable reading of bus and create handle
	h = pi.i2c_open(0, 0x48) #open device at address 0x48 on bus 0
	#Try a first read
	first_db = pi.i2c_read_byte_data(h, 0x0A)
	print ("First db is" + first_db)


	#Set up scheduler to read each second
	def read_db(scheduler);
		#schedule the first call
		scheduler.enter(1, 1 read_db, (scheduler,))
		print("Start reading sound levels")
		#Execute the sound buffer reads
		db = pi.i2c_read_byte_data(h, 0x0A)
		print ("db is" + first_db)


#Execute/schedule 1 second sound readings
scheduled_sound_read=sched.scheduler(time.time, time.sleep)
scheduled_sound_read.enter(1, 1, read_db, (scheduled_sound_read,))
scheduled_sound_read.run()


if __name__ == "__main__":
	main()