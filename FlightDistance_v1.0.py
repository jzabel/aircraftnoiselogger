# FlightDistance.py>

import numpy as np
import math

# constants
#----------
# https://www.unavco.org/software/geodetic-utilities/geoid-height-calculator/geoid-height-calculator.html
homela = 39.+0./60+0./3600. #  reference longitude (adjust 0s in minutes, seconds)
homelo = -105.-0./60-0./3600. # reference longitude (adjust 0s in minutes, seconds)
homeel = 5600. #ft --> *0.3048 = 1707m **NOT IMPLEMENTED**
geodht = -16.67 #m
orthht = 1723.55 #m
Rearth = 6378100. #m
m2ft  = 3.28084 #ft/m
m2mi  = 0.000621371 #mi/m

# functions
#----------

# projectedDistance
#------------------
# reference
#	https://math.stackexchange.com/questions/833002/distance-between-two-points-in-spherical-coordinates
#
# math
# 	dist = {r^2 + r'2 - 2rr'[sin(theta)sin(theta')cos(phi-phi')+cos(theta)cos(theta')]}^1/2
# 	A = r^2 + r'2 --> 2r^2
# 	B = 2rr' --> 2r^2
# 	C = sin(theta)sin(theta')
# 	D = cos(phi-phi')
# 	E = cos(theta)cos(theta')
# 		--> dist = [A - B*(C*D+E)]^1/2
# 		(1,0deg,0deg)spherical = (0,0,1)cartesian --> phi = 90-latitude

def projectedDistance(lat, lon):
    
	A = 2.*(Rearth+orthht+geodht)**2
	B = A
	C = np.sin(np.radians(homelo))*np.sin(np.radians(lon))
	D = np.cos(np.radians((90-homela)-(90-lat)))
	E = np.cos(np.radians(homelo))*np.cos(np.radians(lon))
	dist = math.sqrt(A - B*(C*D + E))*m2mi

#	print("Projected distance: ", dist)

	return dist;

# lineofsightDistance
#------------------
# reference
#	https://math.stackexchange.com/questions/833002/distance-between-two-points-in-spherical-coordinates
#
# math
# 	dist = {r^2 + r'2 - 2rr'[sin(theta)sin(theta')cos(phi-phi')+cos(theta)cos(theta')]}^1/2
# 	A = r^2 + r'2
# 	B = 2rr'
# 	C = sin(theta)sin(theta')
# 	D = cos(phi-phi')
# 	E = cos(theta)cos(theta')
# 		--> dist = [A - B*(C*D+E)]^1/2
# 		(1,0deg,0deg)spherical = (0,0,1)cartesian --> phi = 90-latitude

def lineofsightDistance(lat, lon, geoalt):

	A = (Rearth+orthht+geodht)**2 + (Rearth+geoalt)**2 # REPLACE BARO ALTITDUE WITH GEO ALTITUDE
	B = 2*(Rearth+orthht+geodht)*(Rearth+geoalt)
	C = np.sin(np.radians(homelo))*np.sin(np.radians(lon))
	D = np.cos(np.radians((90-homela)-(90-lat)))
	E = np.cos(np.radians(homelo))*np.cos(np.radians(lon))
	losdist = math.sqrt(A - B*(C*D + E))*m2ft

#	print("Line of sight distance: ", losdist)

	return losdist;