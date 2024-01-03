import googlemaps
import os
from dotenv import load_dotenv

def init_googlemaps_API():
    # Get API parameter from .env file
    load_dotenv()
    GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")

    # Connect to Google Maps API
    try:
        global gmaps
        gmaps= googlemaps.Client(GOOGLE_MAPS_API_KEY)
    except ValueError:
        print('ERROR: Add or check your Google maps API key in local .env file and try again.')
        exit(1)

    return

def get_elevation_from_location(lat_long):
    return gmaps.elevation(lat_long)

def get_elevation_from_address(address):

    # Geocoding an address
    geocode_result = gmaps.geocode(address)

    # Extract the lat/lng from the geocode
    lat = geocode_result[0]['geometry']['location']['lat']
    lng = geocode_result[0]['geometry']['location']['lng']
    location = [(lat, lng)]  # Construct the location dict for elevation

    # Get elevation from the lat/long location
    elevation_result = get_elevation_from_location(location)

    return elevation_result

