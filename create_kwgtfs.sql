CREATE TABLE agency (
	agency_name TEXT,
	agency_url TEXT,
	agency_timezone TEXT,
	agency_lang TEXT,
	agency_phone TEXT
);

CREATE TABLE calendar_dates (
	service_id TEXT,
	date TEXT,
	exception_type INTEGER
);

CREATE TABLE calendar (
	service_id TEXT,
	monday INTEGER,
	tuesday INTEGER,
	wednesday INTEGER,
	thursday INTEGER,
	friday INTEGER,
	saturday INTEGER,
	sunday INTEGER,
	start_date TEXT,
	end_date TEXT
);

CREATE TABLE fare_attributes (
	fare_id INTEGER,
	price REAL,
	currency_type TEXT,
	payment_method INTEGER,
	transfers INTEGER,
	transfer_duration INTEGER
);
CREATE TABLE routes (
	route_id TEXT,
	route_short_name INTEGER,
	route_long_name TEXT,
	route_desc TEXT,
	route_type INTEGER,
	route_url TEXT
);

CREATE TABLE shapes (
	shape_id INTEGER,
	shape_pt_lat REAL,
	shape_pt_lon REAL,
	shape_pt_sequence INTEGER
);

CREATE TABLE stops (
	stop_id INTEGER,
	stop_code INTEGER,
	stop_name TEXT,
	stop_desc TEXT,
	stop_lat REAL,
	stop_lon REAL,
	zone_id INTEGER,
	stop_url TEXT,
	location_type INTEGER,
	parent_station INTEGER
);

CREATE TABLE stop_times (
	trip_id TEXT,
	arrival_time TEXT,
	departure_time TEXT,
	stop_id INTEGER,
	stop_sequence INTEGER,
	pickup_type INTEGER,
	drop_off_type INTEGER
);

CREATE TABLE trips (
	route_id TEXT,
	service_id TEXT,
	trip_id TEXT,
	trip_headsign TEXT,
	direction_id INTEGER,
	block_id INTEGER,
	shape_id INTEGER
);

.separator ,
.import data/calendar.txt calendar
.import data/agency.txt agency
.import data/calendar_dates.txt calendar_dates
.import data/routes.txt routes
.import data/shapes.txt shapes
.import data/stop_times.txt stop_times
.import data/stops.txt stops
.import data/trips.txt trips
