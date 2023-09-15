import smbus


def report_db_level():
	device_bus = 1
	device_addr = 0x48
	bus_handler = smbus.SMBus(device_bus)
	recorded_db = bus_handler.read_byte_data(device_addr, 0x0A)
	current_timestamp = str(datetime.datetime.now())

	return current_timestamp, recorded_db


def main():
	while 1==1:
		current_timestamp, recorded_db = report_db_level()
		print("{}|{}".format(current_timestamp, recorded_db))


if __name__ == "__main__":
	main()
