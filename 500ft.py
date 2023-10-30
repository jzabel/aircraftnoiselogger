# 500ft.py>
# PLOTS NEED WORK - JUST A QUICK MODIFICATION OF InstantantaneousAltitude.py
# Baro altitude referenced to runway should be used instead of geo altitude
# edit hard-coded lat, lon, geo alitude limits as desired

import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from google.cloud import bigquery
from google.oauth2 import service_account

m2ft  = 3.28084 #ft/m

# TODO(developer): Set key_path to the path to the service account key file.
key_path = "/Users/brian/Documents/AirportNoise/github/flight/scripts/superior-noise-loggers-dca5b1ff03b5.json"

credentials = service_account.Credentials.from_service_account_file(
    key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

client = bigquery.Client(credentials=credentials, project=credentials.project_id,)

callsi=np.array([]) # ADS-B callcsign
timepo=np.array([]) # ADS-B time position
lat=np.array([])    # ADS-B latitude
lon=np.array([])    # ADS-B longitude
galt=np.array([])   # ADS-B wgs84 altitude [m]
vel=np.array([])    # ADS-B velocity [UNITS]
vert=np.array([])   # ADS-B vertical rate [UNITS]
   
#N546ND, N522ND

QUERY = """
	SELECT time_position, callsign, latitude, longitude, geo_altitude, velocity, vertical_rate
	FROM `superior-noise-loggers.aircraft_reporting_dataset.opensky-state-vector-reports`
	WHERE SAFE_CAST(latitude AS FLOAT64) > 39.9261 AND SAFE_CAST(latitude AS FLOAT64) < 39.9282 AND SAFE_CAST(longitude AS FLOAT64) < -105.1554 AND SAFE_CAST(longitude AS FLOAT64) > -105.1585 AND SAFE_CAST(geo_altitude AS FLOAT64) < 1833.372
	ORDER BY TIMESTAMP_SECONDS(SAFE_CAST(time_position AS INT64)) DESC
	LIMIT 300
"""
query_job = client.query(QUERY)
rows = query_job.result()
for row in rows:
    callsign = row['callsign']
    time_position = row['time_position']
    latitude = row['latitude']
    longitude = row['longitude']
    geo_altitude = row['geo_altitude']
    velocity = row['velocity']
    vertical_rate = row['vertical_rate']   
    print(f'{callsign} | {time_position} | {latitude} | {longitude} | {geo_altitude} | {velocity} | {vertical_rate}')
    callsi=np.append(callsi,callsign)
    timepo=np.append(timepo,int(time_position))
    lat=np.append(lat,float(latitude))
    lon=np.append(lon,float(longitude))
    galt=np.append(galt,float(geo_altitude))
    vel=np.append(vel,float(velocity))
    vert=np.append(vert,float(vertical_rate))

plt.figure(figsize=(12, 6)) 

dateconv = np.vectorize(datetime.datetime.fromtimestamp)
t = dateconv(timepo)

ax1 = plt.subplot2grid((3, 2), (0,0), colspan=1)
ax1.plot(t, vel, 'o', color='red', label='velocity')
ax1.tick_params(axis='x', bottom=False, labelbottom=False)
ax1.set_ylabel("velocity [UNITS]")
ax1.legend()

ax2 = plt.subplot2grid((3, 2), (1,0), colspan=1)
ax2.plot(lon, lat, 'o', color='green', label='baro. alt.')
ax2.tick_params(axis='x', bottom=False, labelbottom=False)
ax2.set_ylabel("latitude [deg]")
ax2.legend()

ax3 = plt.subplot2grid((3, 2), (2,0), colspan=1)
ax3.plot(t, galt, 'o', color='blue', label='geom. alt.')
ax3.set_ylabel("altitude [m]")
ax3.set_xlabel("local time [DD HH:MM]")
ax3.set_xticklabels(ax2.get_xticks(), rotation = 25)

ax4 = plt.subplot2grid((3, 2), (0,1), rowspan=3)
ax4.plot(t, vert, 'o')
ax4.set_title(callsi[1])
ax4.set_xlabel("local time [DD HH:MM]")
ax4.set_ylabel("vertical rate [UNITS]")
ax4.set_xticklabels(ax3.get_xticks(), rotation = 25)

plt.show(block=False)
plt.savefig('/Users/brian/Documents/AirportNoise/github/flight/results/'+callsign+'.png') 
plt.close()