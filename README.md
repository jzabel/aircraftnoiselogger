# Aircraft Noise Logger

A project to collect noise information from flights over a particular location and send to a consolidated backend

# Links

[Enclosure](Enclosure/README.md)


# Proof of Concept Code Snippets

* [monitor_audio.sh](monitor_audio.sh) - Bash file to access a USB mic and check the root mean square dB level

* [run_monitoring.py](run_monitoring.py) - Runs the bash script and creates a pipe separated entry for timestamp and dB level

* [run_db_monitoring.py](run_db_monitoring.py) - An updated script that reads in information from the new PCBArtist Sound Modules and then prints it to the screen each second as well as publish to our Google Cloud Pubsub backend.

* [send_observation_to_cloud.py](send_observation_to_cloud.py) - Takes obervation data (currently hardcoded) and publishes a Pubsub message to a topic that is linked to a BigQuery export subscription

* [noise-logger-data-schema.avsc](noise-logger-data-schema.avsc) - Avro schema file specifying the table structure for storing observation data

* [requirements.txt](requirements.txt) - Python libraries necessary to authenticate to GCP and publish Pubsub messages

# Code startup & tricks
You must install Google Cloud & Google Cloud Pubsub libraries; however, you need to use older libraries as there isn't yet dependency support in the Raspberry pi libraries for Google Cloud Pubsub version 2.18.4. To start up, follow directions to set up the Google Python libraries including using virtualenv to set up a virtual environment. Then install:
google-cloud-pubsub 2.18.1, 
grpcio 1.56.2 and 
grpcio-status 1.56.2
specifying the versions to use; otherwise, you'll get an error asking for GLIBCXX_3.4.29 in libstdc.so.6.
