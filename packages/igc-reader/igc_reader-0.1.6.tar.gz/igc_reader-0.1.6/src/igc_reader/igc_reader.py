import logging
from datetime import time, datetime, date
from math import radians, cos, sin, asin, sqrt
from tqdm import tqdm

import pandas as pd

from geojson import Feature, Point

logger = logging.getLogger('read_igc')


class read_igc:
	def __init__(self, file_string):
		self.log_entries = []
		self.unread_entries = []
		self.file_string = file_string
		self.flight_recorder = None
		self.track = Track()
		self.task = Task()
		self.infos = FlightInfos()
		self.read_igc()
		self.calculate_parameters()

	@classmethod
	def from_file(cls, file_path):
		if not is_igc(file_path):
			return
		file_string = open(file_path, "r")
		return cls(file_string)

	@classmethod
	def from_file_string(cls, file_string):
		return cls(file_string)

	def read_igc(self):
		for line_number, line in tqdm(enumerate(self.file_string.readlines())):
			if type(line) == bytes:
				line = line.decode('utf-8')
			match line[0]:
				case 'A':  # FR manufacturer and identification
					self.read_a_record(line)
				case 'B':  # Fix
					self.read_b_record(line)
				case 'C':  # Task/declaration
					self.read_c_record(line)
				case 'D':  # Differential GPS
					self.read_d_record(line)
				case 'E':  # Event
					self.read_e_record(line)
				case 'F':  # Constellation
					self.read_f_record(line)
				case 'G':  # Security
					self.read_g_record(line)
				case 'H':  # File Header
					self.read_h_record(line)
				case 'I':  # List of extension data included at end of each fix B record
					self.read_i_record(line)
				case 'J':  # List of data included in each extension(K) Record
					self.read_j_record(line)
				case 'K':  # Extension data
					self.read_k_record(line)
				case 'L':  # Logbook / comments
					self.read_l_record(line)
				case _:  # M,N spare
					logging.debug(f'Invalid entry on line {line_number}: {line}')

	def read_a_record(self, line):
		manufacturer = flight_recorder(line[1:4])
		manufacturer_uid = line[4:7]
		id_extension = line[7:-1]
		self.flight_recorder = f'{manufacturer} {manufacturer_uid} {id_extension}'

	def read_b_record(self, line):
		timestamp = time(int(line[1:3]), int(line[3:5]), int(line[5:7]))
		latitude = float(line[7:9]) + float(f'{line[9:11]}.{line[11:14]}') / 60
		longitude = float(line[15:18]) + float(f'{line[18:20]}.{line[20:23]}') / 60
		p_alt = int(line[25:30])
		gps_alt = int(line[30:35])
		self.track.add_position(timestamp, Position(latitude, longitude), p_alt, gps_alt)

	def read_c_record(self, line):
		if not self.task.is_initialized:
			declaration_time = datetime(
				day=int(line[1:3]),
				month=int(line[3:5]),
				year=(2000 + int(line[5:7])),
				hour=int(line[7:9]),
				minute=int(line[9:11]),
				second=int(line[11:13]))
			intended_date = date(
				year=(2000 + int(line[17:19])),
				day=int(line[13:15]),
				month=int(line[15:17]))
			task_id = int(line[19:23])
			num_tps = int(line[23:25])
			task_description = line[25:-1]
			self.task.initialize(declaration_time, intended_date, task_id, num_tps, task_description)
			return
		latitude = float(line[1:3]) + float(f'{line[3:5]}.{line[5:8]}') / 60
		longitude = float(line[9:12]) + float(f'{line[12:14]}.{line[14:17]}') / 60
		description = line[18:-1]
		self.task.add_turnpoint(Position(latitude, longitude), description)

	def read_d_record(self, line):
		logging.warning(f'D record encountered ({line}). These are not handled at the moment.')
		self.unread_entries.append(line)

	def read_e_record(self, line):
		logging.warning(f'E record encountered ({line}). These are not handled at the moment.')
		self.unread_entries.append(line)

	def read_f_record(self, line):
		logging.warning(f'F record encountered ({line}). These are not handled at the moment.')
		self.unread_entries.append(line)

	def read_g_record(self, line):
		logging.warning(f'G record encountered ({line}). These are not handled at the moment.')
		self.unread_entries.append(line)

	def read_h_record(self, line):
		match line[2:5]:
			case 'DTE':
				self.infos.set_date(line)
			case 'PLT':
				self.infos.set_pilot(line)
			case 'GTY':
				self.infos.set_glider(line)
			case 'GID':
				self.infos.set_glider_id(line)
			case 'DTM':
				self.infos.set_gps_date(line)
			case 'FTY':
				self.infos.set_logging_device(line)
			case 'CCL':
				self.infos.set_competition_class(line)
			case _:
				logging.info(f'H Record {line} could not be interpreted.')
				self.unread_entries.append(line)

	def read_i_record(self, line):
		logging.warning(f'G record encountered ({line}). These are not handled at the moment.')
		self.unread_entries.append(line)

	def read_j_record(self, line):
		logging.warning(f'G record encountered ({line}). These are not handled at the moment.')
		self.unread_entries.append(line)

	def read_k_record(self, line):
		logging.warning(f'G record encountered ({line}). These are not handled at the moment.')
		self.unread_entries.append(line)

	def read_l_record(self, line):
		self.log_entries.append(line)

	def get_coordinates(self):
		coordinates = []
		for p in range(self.track.count):
			coordinates.append([self.track.longitude[p], self.track.latitude[p], self.track.gps_alt[p]])
		return coordinates

	def calculate_parameters(self):
		self.infos.duration = self.track.get_duration()
		self.infos.track_distance = self.track.get_track_length()


def is_igc(file_path):
	if not file_path.lower().endswith('.igc'):
		logging.warning(f'{file_path} is not a .igc file.')
		return False
	else:
		return True


def get_coordinates(file_path, accuracy=4):
	f = open(file_path, "r")
	coordinates = []
	logging.info(f'Reading coordinates from IGC file: {file_path}.')
	if not file_path.lower().endswith('.igc'):
		logging.warning(f'Could not decode {file_path}.')
		return
	try:
		for line in f.readlines():
			if line[0] == 'B':
				lat_deg = float(line[7:9])
				lat_min = float(f'{line[9:11]}.{line[11:14]}')
				lon_deg = float(line[15:18])
				lon_min = float(f'{line[18:20]}.{line[20:23]}')
				altitude = float(line[31:35])
				latitude = lat_deg + lat_min / 60
				longitude = lon_deg + lon_min / 60
				coordinates.append([round(longitude, accuracy), round(latitude, accuracy), altitude])

		logging.debug(f'Decoded {file_path}.')
	except:
		logging.warning(f'Something in {file_path} could not be read.')
	return coordinates


def get_heatmap_points(file_path, accuracy=4, interval=10):
	points = []
	coordinates = get_coordinates(file_path, accuracy)
	if not coordinates:
		return
	for i in range(0, len(coordinates), interval):
		points.append(Feature(geometry=Point(coordinates=tuple(coordinates[i]))))
	return points


def flight_recorder(code):
	codes = {
		'GCS': 'Garrecht',
		'CAM': 'Cambridge Aero Instruments',
		'DSX': 'Data Swan/DSX',
		'EWA': 'EW Avionics',
		'FIL': 'Filser',
		'FLA': 'Flarm(Flight Alarm)',
		'SCH': 'Scheffel',
		'ACT': 'Aircotec',
		'LXN': 'LX Navigation',
		'IMI': 'IMI Gliding Equipment',
		'NTE': 'New Technologies s.r.l.',
		'PES': 'Peschges',
		'PRT': 'Print Technik',
		'SDI': 'Streamline Data Instruments',
		'TRI': 'Triadis Engineering GmbH',
		'WES': 'Westerboer',
		'XXX': 'Other manufacturers',
		'ZAN': 'Zander',
	}
	if (len(code) != 3) or (code not in codes):
		logging.debug(f'{code} is not an official flight recorder code.')
		return code
	else:
		return codes[code]


class Position:
	def __init__(self, latitude, longitude):
		self.latitude = latitude
		self.longitude = longitude

	def is_valid(self):
		if (self.latitude == 0.0) or (self.longitude == 0.0):
			return False
		elif not (-180 < self.longitude < 180):
			return False
		elif not (-90 < self.latitude < 90):
			return False
		return True


class Track:
	def __init__(self):
		self.timestamp = []
		self.latitude = []
		self.longitude = []
		self.p_alt = []
		self.gps_alt = []
		self.count = 0

	def add_position(self, timestamp: time, position: Position, p_alt: int, gps_alt: int):
		self.timestamp.append(timestamp)
		self.latitude.append(position.latitude)
		self.longitude.append(position.longitude)
		self.p_alt.append(p_alt)
		self.gps_alt.append(gps_alt)
		self.count += 1

	def as_df(self):
		df = pd.DataFrame(columns=['timestamp', 'latitude', 'longitude', 'p_altitude', 'gps_altitude'])
		df.timestamp = self.timestamp
		df.latitude = self.latitude
		df.longitude = self.longitude
		df.p_altitude = self.p_alt
		df.gps_altitude = self.gps_alt
		return df

	def get_duration(self):
		first = datetime.combine(date.min, self.timestamp[0])
		last = datetime.combine(date.min, self.timestamp[-1])
		duration = last - first
		return (datetime.min + duration).time()

	def get_track_length(self):
		distance = 0
		lon1 = self.longitude[0]
		lat1 = self.latitude[0]
		alt1 = self.gps_alt[0]
		for i in range(1, self.count):
			lon2 = self.longitude[i]
			lat2 = self.latitude[i]
			alt2 = self.gps_alt[1]
			distance += haversine_alt(lon1, lat1, alt1, lon2, lat2, alt2)
			lon1 = lon2
			lat1 = lat2
			alt1 = alt2
		return distance


class Task:
	def __init__(self):
		self.declaration_time = None
		self.intended_date = None
		self.task_id = None
		self.num_tps = None
		self.task_description = None
		self.latitude = []
		self.longitude = []
		self.description = []
		self.is_initialized = False

	def __str__(self):
		return f'{self.intended_date} {self.task_description} {self.task_id}'

	def initialize(self, declaration_time: datetime, intended_date: date, task_id: int, num_tps: int, description: str):
		self.declaration_time = declaration_time
		self.intended_date = intended_date
		self.task_id = task_id
		self.num_tps = num_tps
		self.task_description = description
		self.is_initialized = True

	def add_turnpoint(self, position: Position, description: str):
		if position.is_valid():
			self.latitude.append(position.latitude)
			self.longitude.append(position.longitude)
			self.description.append(description)

	def as_df(self):
		df = pd.DataFrame(columns=['latitude', 'longitude', 'description'])
		df.latitude = self.latitude
		df.longitude = self.longitude
		df.description = self.description
		return df


class FlightInfos:
	def __init__(self):
		self.date = None
		self.pilot = None
		self.glider = None
		self.glider_id = None
		self.gps_date = None
		self.logging_device = None
		self.competition_class = None
		self.duration = None

	def __str__(self):
		return f'{self.date}-{self.pilot.replace(" ", "")}'

	def set_date(self, line):
		if line[5:10] == 'DATE:':
			self.date = date(day=int(line[10:12]), month=int(line[12:14]), year=(2000 + int(line[14:16])))
		else:
			self.date = date(day=int(line[5:7]), month=int(line[7:9]), year=(2000 + int(line[9:11])))

	def set_pilot(self, line):
		self.pilot = line[19:-1]

	def set_glider(self, line):
		self.glider = line[16:-1]

	def set_glider_id(self, line):
		self.glider_id = line[14:-1]

	def set_gps_date(self, line):
		self.gps_date = line[18:-1]

	def set_logging_device(self, line):
		self.logging_device = line[11:-1]

	def set_competition_class(self, line):
		self.competition_class = line[22:-1]


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