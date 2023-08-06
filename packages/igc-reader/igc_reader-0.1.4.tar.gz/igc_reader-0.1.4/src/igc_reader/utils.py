from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
	"""
	Calculate the great circle distance in kilometers between two points
	on the earth (specified in decimal degrees)
	"""
	# convert decimal degrees to radians
	lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

	# haversine formula
	dlon = lon2 - lon1
	dlat = lat2 - lat1
	a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
	c = 2 * asin(sqrt(a))
	r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
	return c * r

def haversine_alt(lon1, lat1, alt1, lon2, lat2, alt2):
	alt_diff = abs(alt1 - alt2)
	lon_lat_diff = haversine(lon1, lat1, lon2, lat2)
	distance = sqrt(lon_lat_diff**2 + alt_diff**2)
	return distance