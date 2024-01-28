from math import radians, sin, asin, cos, acos, sqrt, atan2, degrees
import sqlite3
import os
from gps import *
import time

gpsd = gps(mode=WATCH_ENABLE) #starting the gps streaming
conn = sqlite3.connect("Airport.db")
cur  = conn.cursor()
my_distance = 0


def get_distance(lat1, lon1, lat2, lon2):
	"""
	Calculate the distance between two points on Earth given their latitude and
	longitude as decimal degrees. Caculations are done using the haversine formula.

	Parameters:
		1 - latitude of position 1
		2 - longitude of position 1
		3 - latitude of position 2
		4 - longitude of position 2
		5 - unit of distance (optional), "miles" or "km", default is "nm" nautical miles

	Returns:
		The distance in whatever unit is specified as a parameter (nautical miles, miles or kilometers)
	"""
	# First set the value of Earth's radius based on desired unit for measuring distance
	earth_radius = 6371008.8/1852   # radius in nautical miles
#	earth_radius = 3958.756  # radius in miles
#	earth_radius = 6371  # radius in kilometers

	# Convert latitude and longitude degrees to radians
	dif_lat = radians(lat2 - lat1)
	dif_lon = radians(lon2 - lon1)
	lat1 = radians(lat1)
	lat2 = radians(lat2)

	a = (sin(dif_lat / 2)**2) + cos(lat1) * cos(lat2) * (sin(dif_lon / 2)**2)

	c = 2 * atan2(sqrt(a), sqrt(1-a))

	distance = earth_radius * c
	return distance




def search(gps_lat, gps_lon):
#	conn = sqlite3.connect("Airport.db")
#	cur  = conn.cursor()

#	cur.execute('SELECT ICAO, LON, LAT  FROM Summary')
	cur.execute('SELECT ICAO, LON, LAT FROM Summary Where (LAT < ? and LAT >  ?) AND (LON < ? and LON > ?)', (gps_lat + 0.248, gps_lat - 0.248, gps_lon + 0.285, gps_lon - 0.285))
	rows  = cur.fetchall()
	conn.commit()

	for ICAO, LON, LAT in rows:
		#print (ICAO, LAT, LON)
		my_distance = get_distance(gpsd.fix.latitude, gpsd.fix.longitude, LAT,LON) # Distance in between my location to Airport
		print ('Distance', '{:1>.2f}'.format(my_distance) + ' nm to ' + ICAO)



def my_location():

	gpsd.next()
	os.system('clear')

	print
	print (' GPS reading')
	print ('----------------------------------------')
	print ('latitude    ' , gpsd.fix.latitude)
	print ('longitude   ' , gpsd.fix.longitude)
	print ('time utc    ' , gpsd.utc,' + ', gpsd.fix.time)
	print ('altitude (meters)' , '{:1>.0f}'.format(gpsd.fix.altitude))
#              print 'eps         ' , gpsd.fix.eps
#              print 'epx         ' , gpsd.fix.epx
#              print 'epv         ' , gpsd.fix.epv
#              print 'ept         ' , gpsd.fix.ept
#              print 'speed (m/s) ' , gpsd.fix.speed
#              print 'climb       ' , gpsd.fix.climb
	print ('track       ' , gpsd.fix.track)
#              print 'mode        ' , gpsd.fix.mode
#              print 'sats        ' , gpsd.satellites

	print ()

	search(gpsd.fix.latitude, gpsd.fix.longitude)

	time.sleep(0.5) #set to whatever

if __name__ == '__main__':
	while True:
		my_location()
