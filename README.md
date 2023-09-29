# Aircraft Noise Logger

## About The Project

A project to collect noise information from flights over a particular location and send to a consolidated backend.

### Prerequisites

It's recommended that you have some experience with Raspberry Pi and a basic understanding of loading packages and running Python scripts.

**Hardware**

- Raspberry Pi Zero 2 W or similar
- Micro SD card (16GB minimum, 32GB recommended)
- 5 volt 2 amp power supply
- [I2C Decibel Sound Level Meter Module](https://pcbartists.com/product/i2c-decibel-sound-level-meter-module/)
- 3D printed [Enclosure](Enclosure/README.md)

**Software**

* [run_db_monitoring.py](run_db_monitoring.py) - This is the core script needed that reads in information from the PCBArtist Sound Modules and then prints it to the screen each second as well as publish to our Google Cloud Pubsub backend.

* [requirements.txt](requirements.txt) - Python libraries necessary to authenticate to GCP and publish Pubsub messages

* [noise-logger-data-schema.avsc](noise-logger-data-schema.avsc) - Avro schema file specifying the table structure for storing observation data

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

### Connect PCB Artist Sound Level Board
Connect the board to the appropriate pins on the Raspberry Pi. [See directions here](https://pcbartists.com/product-documentation/accurate-raspberry-pi-decibel-meter/#connect-decibel-sensor-with-raspberry-pi)

## Usage
* Start the noise meter process on your Pi to run in the background: `nohup python3 run_db_monitoring.py &`

## Running the logger as a service on your Pi

The following instructions will configure your Raspberry Pi to run the `run_db_monitoring.py` script as a service.  This service will automatically run as soon as you boot your device.

**_NOTE_**: This configuration assumes you have configured everything above and your `run_db_monitoring.py` script is in the home directory of the `pi` user in the extracted folder named `aircraftnoiselogger`.  If you created a user other than `pi`, replace the `pi` value in the unit file with the name of the user.

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
ExecStart=/usr/bin/python3 /home/pi/aircraftnoiselogger/run_db_monitoring.py
WorkingDirectory=/home/pi/aircraftnoiselogger
Restart=always
User=pi

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

### TODO:
* Add configuration file for google auth and other params (e.g. location of sensors)
* Add cron setup to automatically start reading

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