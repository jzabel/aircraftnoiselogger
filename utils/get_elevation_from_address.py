import googlemaps
import os
import sys
from dotenv import load_dotenv

# Parse the address passed on command line
if len(sys.argv) > 1:
    address = {sys.argv[1]}
else:
    print('ERROR: Pass the address you would like the elevation - e.g. python3 get_elevation_from_address.py "635 S Snowmass Circle Superior CO"')

print('Input address: ',address)

# Get API parameter from .env file
load_dotenv()
GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")

# Connect to Google Maps
try:
    gmaps = googlemaps.Client(GOOGLE_MAPS_API_KEY)
except ValueError:
    print('ERROR: Add or check your Google maps API key in local .env file and try again.')
    exit(1)

# Geocoding an address
geocode_result = gmaps.geocode(address)

# Extract the lat/lng from the geocode
lat = geocode_result[0]['geometry']['location']['lat']
lng = geocode_result[0]['geometry']['location']['lng']
location = [(lat,lng)]  # Construct the location dict for elevation

elevation_result = gmaps.elevation(location)

print ("SUCCESS! The address ",address," has the following attributes: \r\n",elevation_result)