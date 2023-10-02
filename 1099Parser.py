#!/usr/bin/env python
# encoding: utf-8

import json
import time
import socket
import datetime
import calendar

dataDir = "/home/pi/rawData"

'''
def getLocation():
        resultVar = None
        while resultVar is None:
                try:
                        locationFile = "/home/pi/currentLocation.json"
                        currentLocation = open(locationFile, "r").read()
                        locationObj = json.loads(currentLocation)
                        resultVar = True
                except:
                        pass

        return locationObj
'''

def mkEpoch(inputDatestamp, inputTimestamp):
	inputDatestamp = inputDatestamp.replace("/", "-")
	inputStr = inputDatestamp + " " + inputTimestamp
	datetimeObj = datetime.datetime.strptime(inputStr, "%Y-%m-%d %H:%M:%S.%f")
	epochVal = calendar.timegm(datetimeObj.timetuple())

	return epochVal


def list2obj(rawList):
	outputObj = {}
	outputObj["messageType"] = rawList[0]
	outputObj["transmissionType"] = rawList[1]
	outputObj["sessionId"] = rawList[2]
	outputObj["aircraftId"] = rawList[3]
	outputObj["hexIdent"] = rawList[4]
	outputObj["flightId"] = rawList[5]
	outputObj["loggedDate"] = rawList[6]
	outputObj["loggedTime"] = rawList[7]
	outputObj["loggedEpoch"] = mkEpoch(str(rawList[6]), str(rawList[7]))
	outputObj["generatedDate"] = rawList[8]
	outputObj["generatedTime"] = rawList[9]
	outputObj["generatedEpoch"] = mkEpoch(str(rawList[8]), str(rawList[9]))
	outputObj["callsign"] = rawList[10]
	outputObj["altitude"] = rawList[11]
	outputObj["groundSpeed"] = rawList[12]
	outputObj["track"] = rawList[13]
	outputObj["lat"] = rawList[14]
	outputObj["lon"] = rawList[15]
	outputObj["verticalRate"] = rawList[16]
	outputObj["squawk"] = rawList[17]
	outputObj["alert"] = rawList[18]
	outputObj["emergency"] = rawList[19]
	outputObj["spi"] = rawList[20]
	outputObj["onGround"] = rawList[21]
	outputObj["parsedTime"] = rawList[22]
	return outputObj


def main():

	# print args.accumulate(args.in)
	count_since_commit = 0
	count_total = 0
	count_failed_connection_attempts = 1

	# open a socket connection
	while count_failed_connection_attempts < 10:
		try:
			s = connect_to_socket("localhost", 30003)
			count_failed_connection_attempts = 1
			print ("Connected to dump1090 broadcast")
			break
		except socket.error:
			count_failed_connection_attempts += 1
			print ("Cannot connect to dump1090 broadcast. Making attempt %s." % (count_failed_connection_attempts))
			time.sleep(5.0)
	else:
		quit()

	data_str = ""

	try:
		entryCnt = 0
		#loop until an exception
		while True:
			#get current time
			cur_time = datetime.datetime.utcnow()
			ds = cur_time.isoformat()
			ts = cur_time.strftime("%H:%M:%S")

			# receive a stream message
			try:
				message = ""
				message = s.recv(10)
				data_str += message.strip("\n")
			except socket.error:
				# this happens if there is no connection and is delt with below
				pass

			if len(message) == 0:
				print (ts, "No broadcast received. Attempting to reconnect")
				time.sleep(args.connect_attempt_delay)
				s.close()

				while count_failed_connection_attempts < args.connect_attempt_limit:
					try:
						s = connect_to_socket(args.location, args.port)
						count_failed_connection_attempts = 1
						print ("Reconnected!")
						break
					except socket.error:
						count_failed_connection_attempts += 1
						print ("The attempt failed. Making attempt %s." % (count_failed_connection_attempts))
						time.sleep(args.connect_attempt_delay)
				else:
					quit()

				continue

			# it is possible that more than one line has been received
			# so split it then loop through the parts and validate

			data = data_str.split("\n")

			for d in data:
				line = d.split(",")
				'''
				#if the line has 22 items, it's valid
				if len(line) == 22:
				'''
					# add the current time to the row
					if len(line[14]) > 2:
						#entryCnt += 1
						epochNow = calendar.timegm(time.gmtime())
						line.append(ds)
						tmpObj = {}
						filePath = dataDir + "/" + str(epochNow) + "-" + line[4] + ".json"
						tmpObj["rawData"] = list2obj(line)
						tmpObj["rxLocation"] = getLocation()
						print tmpObj["rxLocation"]
						try:
							open(filePath, "wb").write(json.dumps(tmpObj))
						except:
                                                        print "Error retrieving receiver location..."
							pass
						#print line
						#print entryCnt

					# since everything was valid we reset the stream message
					data_str = ""
				'''
				#else:
					# the stream message is too short, prepend to the next stream message
					#data_str = d
					#continue
				'''

	except KeyboardInterrupt:
		print ("\n%s Closing connection" % (ts,))
		s.close()

		conn.commit()
		conn.close()
		print (ts, "%s squitters added to your database" % (count_total,))

	except Exception as e:
		print (e)
		quit()

def connect_to_socket(loc,port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((loc, port))
	return s


if __name__ == '__main__':
	main()
