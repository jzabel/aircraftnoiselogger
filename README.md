# Aircraft Noise Logger

A project to collect noise information from flights over a particular location and send to a consolidated backend

# Links

[Enclosure](Enclosure/README.md)


# Proof of Concept Code Snippets

* [monitor_audio.sh](monitor_audio.sh) - Bash file to access a USB mic and check the root mean square dB level

* [run_monitoring.py](run_monitoring.py) - Runs the bash script and creates a pipe separated entry for timestamp and dB level

* [run_db_monitoring.py](run_db_monitoring.py) - An updated script that reads in information from the new PCBArtist Sound Modules and then prints it to the screen each second. To initialize, you must either 1/ start the pigpio daemon prior calling "sudo pigpiod" from the command line, or alternatively add that command to the root crontab for startup initialization.

* [send_observation_to_cloud.py](send_observation_to_cloud.py) - Takes obervation data (currently hardcoded) and publishes a Pubsub message to a topic that is linked to a BigQuery export subscription

* [noise-logger-data-schema.avsc](noise-logger-data-schema.avsc) - Avro schema file specifying the table structure for storing observation data

* [requirements.txt](requirements.txt) - Python libraries necessary to authenticate to GCP and publish Pubsub messages
