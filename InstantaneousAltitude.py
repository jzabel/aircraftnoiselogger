# InstantaneousAltitude.py>
# https://gis.stackexchange.com/questions/338392/getting-elevation-for-multiple-lat-long-coordinates-in-python
# THIS CODE IS SLOW AND ONLY SO MANY QUERIES PER DAY CURRENTLY; WE SHOULD GENERATE OUR OWN TOPO MAP TO BE SAVED TO BIG QUERY OR TO LOCAL MACHINES
# PLOTS NEED CLEANUP

import datetime
import requests
import urllib
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

# USGS Elevation Point Query Service
#url = r'https://nationalmap.gov/epqs/pqs.php?'
#new 2023:
url = r'https://epqs.nationalmap.gov/v1/json?'

def elevation_function(df, lat_column, lon_column):
    """Query service using lat, lon. add the elevation values as a new column."""
    elevations = []
    for lat, lon in zip(df[lat_column], df[lon_column]):
                
        # define rest query params
        params = {
            'output': 'json',
            'x': lon,
            'y': lat,
            'units': 'Meters'
        }
        
        # format query string and return query value
        result = requests.get((url + urllib.parse.urlencode(params)))
        #elevations.append(result.json()['USGS_Elevation_Point_Query_Service']['Elevation_Query']['Elevation'])
        #new 2023:
        elevations.append(result.json()['value'])

    df['elev_meters'] = elevations

    return df;

callsi=np.array([]) # ADS-B callcsign
icao=np.array([]) # ADS-B icao24
timepo=np.array([]) # ADS-B time position
lat=np.array([])    # ADS-B latitude
lon=np.array([])    # ADS-B longitude
balt=np.array([])   # ADS-B barometric altitude [m]
galt=np.array([])   # ADS-B wgs84 altitude [m]
hagl=np.array([])   # height above ground level [ft]
   
#N546ND, N522ND

QUERY = """
    SELECT callsign, icao24, time_position, latitude, longitude, baro_altitude, geo_altitude
    FROM `superior-noise-loggers.aircraft_reporting_dataset.opensky-state-vector-reports`
    WHERE callsign = 'CXK159'
    GROUP BY callsign, icao24, time_position, latitude, longitude, baro_altitude, geo_altitude
    ORDER BY icao24, time_position
    DESC LIMIT 10
"""
query_job = client.query(QUERY)
rows = query_job.result()
for row in rows:
    callsign = row['callsign']
    icao24 = row['icao24']
    time_position = row['time_position']
    latitude = row['latitude']
    longitude = row['longitude']
    baro_altitude = row['baro_altitude']
    geo_altitude = row['geo_altitude']    
    print(f'{callsign} | {icao24} | {time_position} | {latitude} | {longitude} | {baro_altitude} | {geo_altitude}')
    callsi=np.append(callsi,callsign)
    icao=np.append(icao,icao24)
    timepo=np.append(timepo,int(time_position))
    lat=np.append(lat,float(latitude))
    lon=np.append(lon,float(longitude))
    balt=np.append(balt,float(baro_altitude))
    galt=np.append(galt,float(geo_altitude))

# create data frame
df = pd.DataFrame({'lat': lat,'lon': lon})
elevation_function(df, 'lat', 'lon')
df.head()
elevation = np.array(df.elev_meters)
print(df)

for i,item in enumerate(galt):
    elevation[i] = float(elevation[i])
    hagl=np.append(hagl,(balt[i]-float(df.elev_meters[i]))*m2ft)

plt.figure(figsize=(12, 6)) 

dateconv = np.vectorize(datetime.datetime.fromtimestamp)
t = dateconv(timepo)

print(type(t[1]))
print(type(elevation[1]))
print(type(balt[1]))
print(type(galt[1]))
print(type(hagl[1]))

# plt.subplot(1, 2, 1)
# plt.plot(t, elevation, color='red', label='elevation')
# plt.plot(t, balt, color='green', label='baro. alt.')
# plt.plot(t, galt, color='blue', label='geom. alt.')
# plt.title(icao[1]+" "+callsi[1])
# plt.xlabel("local time [DD HH:MM]")
# plt.ylabel("altitude, elevation [m]")
# plt.xticks( rotation=25 )
# plt.legend()
# plt.ylim(min(elevation),max(np.maximum(balt,galt)))

# plt.subplot(1, 2, 2)
# plt.plot(t, hagl)
# plt.title(icao[1]+" "+callsi[1])
# plt.xlabel("local time [DD HH:MM]")
# plt.ylabel("HAGL [ft]")
# plt.xticks( rotation=25 )

ax1 = plt.subplot2grid((3, 2), (0,0), colspan=1)
ax1.plot(t, elevation, 'o', color='red', label='elevation')
ax1.tick_params(axis='x', bottom=False, labelbottom=False)
ax1.set_ylabel("elevation [m]")
ax1.legend()

ax2 = plt.subplot2grid((3, 2), (1,0), colspan=1)
ax2.plot(t, balt, 'o', color='green', label='baro. alt.')
ax2.tick_params(axis='x', bottom=False, labelbottom=False)
ax2.set_ylabel("altitude [m]")
ax2.legend()

ax3 = plt.subplot2grid((3, 2), (2,0), colspan=1)
ax3.plot(t, galt, 'o', color='blue', label='geom. alt.')
ax3.set_ylabel("altitude [m]")
ax3.set_xlabel("local time [DD HH:MM]")
ax3.set_xticklabels(ax2.get_xticks(), rotation = 25)

ax4 = plt.subplot2grid((3, 2), (0,1), rowspan=3)
ax4.plot(t, hagl, 'o')
ax4.set_title(icao[1]+" "+callsi[1])
ax4.set_xlabel("local time [DD HH:MM]")
ax4.set_ylabel("HAGL [ft]")
ax4.set_xticklabels(ax3.get_xticks(), rotation = 25)

# plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4,hspace=0.4)
# # plt.rcParams['figure.constrained_layout.use'] = True
 
plt.show(block=False)
plt.savefig('/Users/brian/Documents/AirportNoise/github/flight/results/'+callsign+'_'+icao24+'.png') 
plt.close()

