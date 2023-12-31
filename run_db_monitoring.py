import json
import time
import datetime
import smbus
import sched
from google.cloud import pubsub_v1
from google.oauth2 import service_account

config_filename = "config.json"

# Method to load config file
def load_config(filename):
    try:
        with open(filename, 'r') as config_file:
            config = json.load(config_file)
        return config
    except FileNotFoundError:
        print(f"Config file '{filename}' not found.")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in '{filename}': {e}")
        exit(1)

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

	#print ("db is " + str(recorded_db) + ' @ ' + current_timestamp)

	reporting_obj = {
		"reporting_station": reporting_station,
		"reporting_timestamp": current_timestamp,
		"db_report": float(recorded_db)
	}

	publish_data(reporting_obj)

	return current_timestamp, recorded_db


def main():
	try:
		print("Starting up")

		# Execute/schedule 1 second sound readings
		scheduled_sound_read = sched.scheduler(time.time, time.sleep)
		scheduled_sound_read.enter(1, 1, read_db, (scheduled_sound_read,))
		print("Start reading sound levels")
		scheduled_sound_read.run()

	except Exception as e:
		print("encountered an issue - not publishing")
		print(f"An exception occurred: {e}")
		exit(1)


if __name__ == "__main__":
	config = load_config(config_filename)
	credentials_file = config["credentialsFile"]
	credentials_obj = service_account.Credentials.from_service_account_file(credentials_file)
	project_id = config["projectId"]
	pubsub_topic = config["topicId"]
	reporting_station = config["reportingStation"]
	
	main()
