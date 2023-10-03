# Aircraft Noise Logger

## About The Project

A project to collect noise information from flights over a particular location and send to a consolidated backend.
There are three components to this project: 
1/ instructions and code to build and deploy a number of "noise sensors" throughout an area. These internet of things (IOT) sensors are capable of measuring the dB and sending information regarding that measurement to back-end service (in this case Google Cloud) for storage and analysis.
2/ A system to log aircraft overflights over a defined area and store them in Google cloud for analysis
3/ Logic and analysis using both sound and flight data to answer impact questions regarding air traffic and noise

## Logic and Analysis
All data is currently stored in BigQuery in a noise_logging_dataset and an aircraft_reporting_dataset. Each of these datasets share a common key in the form of a timestamp. 

In the noise_logging_observations, the code places entries each second (1Hz) with a key of "reporting_station" and "reporting_timestamp." Each of these keys has a db_report with value.

In the aircraft_reporting_dataset, each aircraft entering the zone of interest is logged into the dataset with keys of time_position, callsign, latitude, longitude, geo_altitude, baro_altitude, and additional information.

A third table stores callsign ("N number") data, plane type, registrant information, etc.

### Questions to answer
Here are questions we wish to answer and visualize with this information. Github issues have been created for each. Each response should attempt to detail date/time, plane (callsign), type of aircraft, db impact, and geo_altitude. Please use the Github issue to coordinate answering them:
1. [Number of Flights over Rock Creek Superior by callsign each day with corresponding noise impact.](https://github.com/jzabel/aircraftnoiselogger/issues/11)
2. [Total number of touch and go operations by plane and by time/date.](https://github.com/jzabel/aircraftnoiselogger/issues/12)
3. [Noise impact by type of plane and altitude at various measurement points and/or by altitude](https://github.com/jzabel/aircraftnoiselogger/issues/13)
4. [Planes flying below 500ft over the residential area](https://github.com/jzabel/aircraftnoiselogger/issues/14)
5. [Planes louder than 60dB over the residential area (frequency, largest impacts, etc.)](https://github.com/jzabel/aircraftnoiselogger/issues/15)
6. [Generate FAA DNL style measurements using actual data](https://github.com/jzabel/aircraftnoiselogger/issues/16)

Please reach out via an issue to access project data and cloud environment.

## Flight Capture Information
To capture flight data, we ultimately decided on a hybrid approach between directly capturing ADSB messages and easier access of an API-based solution. After some digging, we decided to create one central server to publish flight information to a centralized database which all clients, analysts, etc. can access as the truth for plane overflights. To do so, we created multiple Raspberry Pi receivers in the area to capture ADSB messages via Dump1090 and then publish them to the OpenSky API. We have a few in the area, but ultimately only need one to two with good positions / antenna. 

These PIs are responsible for sending ADSB messages to OpenSky. When testing messages, we saw about 1.9M messages in 3 hours from ADSB in our area. As such, relying on OpenSky to consolidate, fill in, update, etc. is very helpful. Because we contribute to OpenSky API, we get increased call limits and we can call data from our own sensors without limits.

As such, one of the Raspberry Pi units is responsible for calling OpenSkyAPI to retrieve flights our ADSB sensors is measuring, do some filtering to include only those in the region of interest, and then publish to our database for analysis.

To get ADSB sensors up and running, you need:
1. Install Dump1090. [This guide is comprehensive in getting this running.](https://stfuandfish.com/2021/10/10/rtl-sdr-dump1090-build-and-install-raspberry-pi-a-video-companion-article/). [This guide](https://vortac.io/2020/06/02/installing-dump1090-on-raspberrypi/) is also helpful if you run into issues.
2. Then sign up to send your ADSB messages to OpenSky for processing. [You can sign up and set your receiver here.](https://opensky-network.org/community/projects/30-dump1090-feeder)

Finally, configure one of your ADSB feeders to query and publish information for processing in the zone of interest. This script is responsible for that publishing:
* [QueryFlight Script](/flight_logger/queryFlights.py) - queries and filters flights in the region of interest, publishing them to Google PubSub and ultimately into Google BigQuery for analysis.


## Noise Sensor Loggers -
See instructions below on how to build and produce sensors capable of monitoring and logging noise measurements:

### Prerequisites

It's recommended that you have some experience with Raspberry Pi and a basic understanding of loading packages and running Python scripts.

**Hardware**

- Raspberry Pi Zero 2 W or similar
- Micro SD card (16GB minimum, 32GB recommended)
- 5 volt 2 amp power supply
- [I2C Decibel Sound Level Meter Module](https://pcbartists.com/product/i2c-decibel-sound-level-meter-module/)
- 3D printed [Enclosure](Enclosure/README.md)

**Software**

* [run_db_monitoring.py](run_db_monitoring.py) - This is the core script needed that reads in information from the PCBArtist Sound Modules and is responsible for publishing it to the Google Cloud backend. Publishing occurs by pushing data to a Google Pub/Sub channel which in turn then feeds to a consolidated Google BigQuery table.

* [requirements.txt](requirements.txt) - Python libraries necessary to authenticate to GCP and publish Pubsub messages. See notes below as it relates to version information and compatibility with Raspberry Pi OS for Google PubSub python libraries.

* [noise-logger-data-schema.avsc](noise-logger-data-schema.avsc) - Avro schema file specifying the table structure for storing observation data (set in Google PubSub).

### Installation / Getting Started

**Raspberry Pi Setup**
* Create the base operating system using the current version of Raspberry Pi OS (previously Raspbian). Raspberry Pi OS with desktop works great (although is overkill). At development time, we used Kernel 6.1, Debian version 11 (bullseye). [Details on installing here](https://www.raspberrypi.com/software/)

**NOTE:** We recommend installing the "Raspberry Pi OS Lite (32 bit)" image.

Once booted, you need to load libraries and requirements.

### Loading libraries and requirements
#### Update current libraries:
Run `sudo apt-get update && sudo apt-get upgrade`

#### Enable the I2C interface
See: [Enable I2C Interface on the Raspberry Pi](https://www.raspberrypi-spy.co.uk/2014/11/enabling-the-i2c-interface-on-the-raspberry-pi/)

#### Make sure `pip3` is installed.  
If not use the command: `sudo apt-get install python3-pip`

#### Download code from repo
Copy code from this repo into the home `~/` directory of your Pi:
* From a terminal use the following
    - Get the files from the repository: `wget -P ~/ "https://github.com/jzabel/aircraftnoiselogger/archive/master.zip"`
    - Unpack the files into a directory: `unzip master.zip -d aircraftnoiselogger`

#### Setup a virtual environment
Make sure to set up a virtual environment where `<your-env>` is an environment value you set like `aircraft-logger-env`.

```
sudo pip3 install virtualenv
virtualenv <your-env>
source <your-env>/bin/activate
```

_example:_
    
```
sudo pip3 install virtualenv
virtualenv aircraft-logger-env 
source aircraft-logger-env/bin/activate
```


* Install required libraries run `sudo pip3 install -r requirements.txt`.
* Change the location of your google auth.json key in run_db_monitoring.py 

#### Adjust your configuration file
The config.json file holds the key values for where to find Google publishing credentials, PubSub topic and projectID, and sets the name of the reporting station. Modify this file to point to the location of your credential file, adjust if necessary the pub/sub topic and project, and set the correct reportingStation name to identify the particular logger.
[Configuration file](config.json)

### Connect PCB Artist Sound Level Board
Connect the board to the appropriate pins on the Raspberry Pi. [See directions here](https://pcbartists.com/product-documentation/accurate-raspberry-pi-decibel-meter/#connect-decibel-sensor-with-raspberry-pi)

## Usage
* Preferred is to set up a service to keep the process running (see below); however you can test or run the script by running the script in the background: `nohup python3 run_db_monitoring.py &` or by simply calling `python3 run_db_monitoring.py`

## Running the logger as a service on your Pi

The following instructions will configure your Raspberry Pi to run the `run_db_monitoring.py` script as a service.  This service will automatically run as soon as you boot your device.

**_NOTE_**: This configuration assumes you have configured everything above and your `run_db_monitoring.py` script is in the home directory of the `pi` user in the extracted folder named `aircraftnoiselogger`.

### 1. Create a systemd service unit file:

Create a new .service file named `aircraftnoiselogger_script.service`, in the `/etc/systemd/system/` directory:

```
sudo nano /etc/systemd/system/aircraftnoiselogger_script.service
```

### 2. Add the following content to the service unit file:

```
[Unit]
Description=Aircraft Noise Logging Python Script Service
After=network.target

[Service]
ExecStart=/home/pi/aircraftnoiselogger/aircraft-logger-env/bin/python3 /home/pi/aircraftnoiselogger/run_db_monitoring.py
WorkingDirectory=/home/pi/aircraftnoiselogger
Restart=always
User=pi
Environment=PATH=/home/pi/aircraftnoiselogger/aircraft-logger-env/bin
Environment=PYTHONPATH=/home/pi/aircraftnoiselogger

[Install]
WantedBy=multi-user.target
```

Save the file and exit the text editor (in Nano, press `Ctrl+O`, then Enter, and `Ctrl+X`).

### 4. Reload systemd to read the new service file:

```
sudo systemctl daemon-reload
```

### 5. Enable the service to start on boot:

```
sudo systemctl enable aircraftnoiselogger_script.service
```

### 6. Start the service:

```
sudo systemctl start aircraftnoiselogger_script.service
```

To check the status of your service and see if it's running without errors, you can use:

```
sudo systemctl status aircraftnoiselogger_script.service
```


### Proof of Concept Code Snippets
Moved proof of concept and development scrips to the POC folder. The following scripts are no longer used, but left in case helpful.

* [monitor_audio.sh](monitor_audio.sh) - Bash file to access a USB mic and check the root mean square dB level
* [run_monitoring.py](run_monitoring.py) - Runs the bash script and creates a pipe separated entry for timestamp and dB level
* [send_observation_to_cloud.py](send_observation_to_cloud.py) - Takes observation data (currently hardcoded) and publishes a Pubsub message to a topic that is linked to a BigQuery export subscription

### Noise / Audio data

See: [ACCURATE RASPBERRY PI DECIBEL METER](https://pcbartists.com/product-documentation/accurate-raspberry-pi-decibel-meter/)

### Code startup & tricks
You must install Google Cloud & Google Cloud Pubsub libraries; however, you need to use older libraries as there isn't yet dependency support in the Raspberry pi libraries for Google Cloud Pubsub version 2.18.4. To start up, follow directions to set up the Google Python libraries including using virtualenv to set up a virtual environment. This is set automatically in the requirements.txt. If you use current versions, you'll get an error asking for GLIBCXX_3.4.29 in libstdc.so.6.

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

## Acknowledgments

[TODO]

* []()
* []()
* []()