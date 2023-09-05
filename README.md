# Aircraft Noise Logger

A project to collect noise information from flights over a particular location and send to a consolidated backend

# Links

[Enclosure](Enclosure/README.md)


# Proof of Concept Code Snippets

* [monitor_audio.sh](monitor_audio.sh) - Bash file to access a USB mic and check the root mean square dB level

* [run_monitoring.py](run_monitoring.py) - Runs the bash script and creates a pipe separated entry for timestamp and dB level

* [send_observation_to_cloud.py](send_observation_to_cloud.py) - Takes obervation data (currently hardcoded) and publishes a Pubsub message to a topic that is linked to a BigQuery export subscription
