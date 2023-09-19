import json
import time
import datetime
import smbus
import sched
from google.cloud import pubsub_v1
from google.oauth2 import service_account


credentials_obj = service_account.Credentials.from_service_account_file(
	"/home/jeff/dev/noise-logger/superior-noise-loggers-daa6617f2476.json"
)

project_id = "superior-noise-loggers"
pubsub_topic = "noise-logger-ingest"


def publish_data(reporting_obj):
	publisher_client = pubsub_v1.PublisherClient(credentials = credentials_obj)

	pubsub_topic_path = "projects/{project_id}/topics/{pubsub_topic}".format(
		project_id = project_id,
		pubsub_topic = pubsub_topic
	)

	async_future = publisher_client.publish(
		pubsub_topic_path,
		json.dumps(reporting_obj).encode("utf-8")
 	)

	async_future.result()

	return "data published"


def read_db(scheduler):

	device_bus = 1
	device_addr = 0x48
	bus_handler = smbus.SMBus(device_bus)
	recorded_db = bus_handler.read_byte_data(device_addr, 0x0A)
	current_timestamp = str(datetime.datetime.now())

	#schedule the first call
	scheduler.enter(1, 1, read_db, (scheduler,))

	print ("db is " + str(recorded_db) + ' @ ' + current_timestamp)

	reporting_obj = {
		"reporting_station": "zabel_flint",
		"reporting_timestamp": current_timestamp,
		"db_report": float(recorded_db)
	}

	publish_data(reporting_obj)

	return current_timestamp, recorded_db


def main():
	try:
		try:
			while 1==1:
				print ("Starting up")

				#Execute/schedule 1 second sound readings
				scheduled_sound_read=sched.scheduler(time.time, time.sleep)
				scheduled_sound_read.enter(1, 1, read_db, (scheduled_sound_read,))
				print("Start reading sound levels")
				scheduled_sound_read.run()
		except:
	 		print("encountered an issue - not publishing")
	except KeyboardInterrupt:
		print("Breaking out...")


if __name__ == "__main__":
	main()
