# Aircraft Noise Logger

## About The Project

A project to collect noise information from flights over a particular location and send to a consolidated backend

### Built With

[TODO]

## Getting Started

[TODO]

### Prerequisites

**Hardware**

- Raspberry Pi Zero 2 W
- [I2C Decibel Sound Level Meter Module](https://pcbartists.com/product/i2c-decibel-sound-level-meter-module/)
- 3D printed [Enclosure](Enclosure/README.md)

**Software**

[TODO]

### Installation

[TODO]

## Usage

See: [ACCURATE RASPBERRY PI DECIBEL METER](https://pcbartists.com/product-documentation/accurate-raspberry-pi-decibel-meter/)

### Proof of Concept Code Snippets

* [monitor_audio.sh](monitor_audio.sh) - Bash file to access a USB mic and check the root mean square dB level

* [run_monitoring.py](run_monitoring.py) - Runs the bash script and creates a pipe separated entry for timestamp and dB level

* [run_db_monitoring.py](run_db_monitoring.py) - An updated script that reads in information from the new PCBArtist Sound Modules and then prints it to the screen each second as well as publish to our Google Cloud Pubsub backend.

* [send_observation_to_cloud.py](send_observation_to_cloud.py) - Takes obervation data (currently hardcoded) and publishes a Pubsub message to a topic that is linked to a BigQuery export subscription

* [noise-logger-data-schema.avsc](noise-logger-data-schema.avsc) - Avro schema file specifying the table structure for storing observation data

* [requirements.txt](requirements.txt) - Python libraries necessary to authenticate to GCP and publish Pubsub messages

### Code startup & tricks
You must install Google Cloud & Google Cloud Pubsub libraries; however, you need to use older libraries as there isn't yet dependency support in the Raspberry pi libraries for Google Cloud Pubsub version 2.18.4. To start up, follow directions to set up the Google Python libraries including using virtualenv to set up a virtual environment. Then install:
google-cloud-pubsub 2.18.1, 
grpcio 1.56.2 and 
grpcio-status 1.56.2
specifying the versions to use; otherwise, you'll get an error asking for GLIBCXX_3.4.29 in libstdc.so.6.


## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

[TODO]

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

## Contact

[TODO]

## Acknowledgments

[TODO]

* []()
* []()
* []()