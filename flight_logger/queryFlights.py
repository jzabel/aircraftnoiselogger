import time
import threading 
import json
import requests
from opensky_api import OpenSkyApi
from google.cloud import pubsub_v1
from google.oauth2 import service_account

credentials_obj = service_account.Credentials.from_service_account_file(
	#Modify for pubsub key location
	#"../superior-noise-loggers.json"
)

project_id = "superior-noise-loggers"
pubsub_topic = "opensky-state-vector-ingest"
baseURL = "https://opensky-network.org/api"
ownStates = "/states/own"
username ="jzabel"
#Modify below to put in opensky password
pw = "replacePasswordHere"

opensky_state_keys = [
	"icao24",
	"callsign",
	"origin_country",
	"time_position",
	"last_contact",
	"longitude",
	"latitude",
	"baro_altitude",
	"on_ground",
	"velocity",
	"true_track",
	"vertical_rate",
	"sensors",
	"geo_altitude",
	"squawk",
	"spi",
	"position_source",
	"category",
]


class RepeatedTimer(object):
  def __init__(self, interval, function, *args, **kwargs):
    self._timer = None
    self.interval = interval
    self.function = function
    self.args = args
    self.kwargs = kwargs
    self.is_running = False
    self.next_call = time.time()
    self.start()

  def _run(self):
    self.is_running = False
    self.start()
    self.function(*self.args, **self.kwargs)

  def start(self):
    if not self.is_running:
      self.next_call += self.interval
      self._timer = threading.Timer(self.next_call - time.time(), self._run)
      self._timer.start()
      self.is_running = True

  def stop(self):
    self._timer.cancel()
    self.is_running = False

def opensky_api(call):

	r = requests.get(
		baseURL + call,
		auth=(username, pw)
		)
	if r.status_code == 200:
		return r.json()
	else:
			print("Response not OK. Status {0:d} - {1:s}".format(r.status_code, r.reason))

	return None

def publish_flight(flight):
	for keys in flight:
		flight[keys] = str(flight[keys])

	#print(flight)

	publisher_client = pubsub_v1.PublisherClient(credentials = credentials_obj)

	pubsub_topic_path = "projects/{project_id}/topics/{pubsub_topic}".format(
		project_id = project_id,
		pubsub_topic = pubsub_topic
	)

	#Publish flight
	async_future = publisher_client.publish(
		pubsub_topic_path,
		json.dumps(flight).encode("utf-8")
 	)
	#print(json.dumps(flight))

	async_future.result()

	return "data published"

def process_local_flights(states):

	#Let's filter flights

	planes = 0
	ignored_planes = 0

	if(states['states'] is not None):
		for state in states['states']:
			# Add keys into new json string
			plane_dict = {k:v for k,v in zip(opensky_state_keys, state)}
			plane_dict['sensors'] = '"' + str(plane_dict['sensors']) + '"'

			#Now filter out for just our region
			if(plane_dict['longitude'] is not None and plane_dict['latitude'] is not None and plane_dict['geo_altitude'] is not None):
				if (plane_dict['longitude'] < -105.076992 and plane_dict['longitude'] > -105.165851 and 
					plane_dict['latitude']  > 39.873575 and plane_dict['latitude']  < 39.946902 and
					plane_dict['geo_altitude'] < 7500):
					#Since all conditions are true we should add this plane
					#print ("plan dict")
					#print(plane_dict)
					planes += 1
					# Send to publisher
					publish_flight(plane_dict)
				else:
					ignored_planes += 1

		print("Found " + str(planes) + " in region and ignored " + str(ignored_planes))

	return planes

def getSystemFlights(api_nologin):

	print("Getting system flights")
	all_planes = api_nologin.get_states(bbox=(39.873575, 39.946902,-105.165851, -105.076992))
	#process into array 
	planes = 0
	if(all_planes is not None):
		for plane in all_planes.states:
			plane_dict = {k:v for k,v in zip(opensky_state_keys, plane)}
			plane_dict['sensors'] = '"' + str(plane_dict['sensors']) + '"'
			planes += 1
			publish_flight(plane_dict)

	#Publish them
	print("SYSYTEM-FLIGHTS. Found " + str(planes) + " in system and published them")

	return planes


def getOwnFlights(api):

	# Overall code
	my_states = opensky_api(ownStates)
	local_planes = process_local_flights(my_states)

	return local_planes


def main():


	api = OpenSkyApi(username, pw)
	api_nologin = OpenSkyApi()

	## Bounding box around airport
	#NW (39.946902, -105.165851)
	#NE (39.946902, -105.076992)
	#SE (39.873575, -105.076992)
	#SW (39.873575, -105.165851)

	## 20 mile bounding box

	print ("Starting up")

	ownFlights = RepeatedTimer(1, getOwnFlights, api)
	#allFlights = RepeatedTimer(261, getSystemFlights, api_nologin)


if __name__ == "__main__":
	main()