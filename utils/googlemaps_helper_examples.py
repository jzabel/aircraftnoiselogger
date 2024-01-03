
import googlemaps_helper

# Initialize the Google Maps API interface
googlemaps_helper.init_googlemaps_API()

"""
EXAMPLE 1:  get_elevation_from_address(address)
    Description:    Determine the elevation and location data by passing in an address  
    Input:          'address' in the form of a string that you would enter into Google Maps
    Returns:        A Location object with the following elements:
                        ['elevation'] - the elevation of the address in meters
                        ['location'] - the lat/long of the address in {['lat'],['lng']} form
                        ['resolution'] -   The value indicating the maximum distance between data points from which the elevation was interpolated, in meters.
                    See https://developers.google.com/maps/documentation/elevation/requests-elevation for more context

"""
# Set the address you are interested in determining the elevation of.  In this case the address is in Superior CO so we
# would expect the elevation to be ~1600m or ~5280 feet
address = '1500 Coalton Rd, Superior, CO 80027'  # Superior Community Center address
elevation_result_1 = googlemaps_helper.get_elevation_from_address(address)
print("Example 1: The address ", address, " has the following attributes: \r\n", elevation_result_1)

"""
EXAMPLE 2:  get_elevation_from_location(lat_long):
    Description:    Determine the elevation and location data by passing in an lat/long struct   
    Input:          'lat_long' in the form of a object
    Returns:        A Location object with the same elements as Example 1
"""
# Constuct the lat/long pair you would like to get the elevation of
lat_long = [(39.92823,-105.14846)]  # Location of Superior Community Center
elevation_result_2 = googlemaps_helper.get_elevation_from_location(lat_long)
print("Example 2: The location ", lat_long, " has the following attributes: \r\n", elevation_result_2)
