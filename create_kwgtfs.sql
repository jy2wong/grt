CREATE TABLE agency (
	agency_phone TEXT,
	agency_url TEXT,
	agency_id TEXT,
	agency_name TEXT,
	agency_timezone TEXT,
	agency_lang TEXT
);

CREATE TABLE calendar_dates (
	service_id TEXT,
	date TEXT,
	exception_type INTEGER
);

CREATE TABLE calendar (
	service_id TEXT,
	start_date TEXT,
	end_date TEXT,
	monday INTEGER,
	tuesday INTEGER,
	wednesday INTEGER,
	thursday INTEGER,
	friday INTEGER,
	saturday INTEGER,
	sunday INTEGER
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
	route_long_name TEXT,
	route_id INTEGER,
	route_type INTEGER,
	route_text_color TEXT,
	agency_id TEXT,
	route_color TEXT,
	route_url TEXT,
	route_desc TEXT,
	route_short_name INTEGER
);

CREATE TABLE shapes (
	shape_id INTEGER,
	shape_pt_lat REAL,
	shape_pt_lon REAL,
	shape_pt_sequence INTEGER,
	shape_dist_traveled REAL
);

CREATE TABLE stops (
	stop_lat REAL,
	stop_code INTEGER,
	stop_lon REAL,
	stop_id TEXT,
	stop_url TEXT,
	parent_station INTEGER,
	stop_desc TEXT,
	stop_name TEXT,
	location_type INTEGER,
	zone_id INTEGER
);

CREATE TABLE stop_times (
	trip_id INTEGER,
	arrival_time TEXT,
	departure_time TEXT,
	stop_id INTEGER,
	stop_sequence INTEGER,
	stop_headsign TEXT,
	pickup_type INTEGER,
	drop_off_type INTEGER,
	shape_dist_traveled TEXT
);

CREATE TABLE trips (
	block_id TEXT,
	route_id INTEGER,
	direction_id INTEGER,
	trip_headsign TEXT,
	shape_id INTEGER,
	service_id TEXT,
	trip_id INTEGER
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

CREATE TABLE stop_lookup AS
	SELECT trips.service_id, stop_times.arrival_time,
		   stops.stop_name, trips.trip_headsign,
	       stops.stop_id,
		   calendar.*
	FROM stop_times
	INNER JOIN trips ON stop_times.trip_id = trips.trip_id
	INNER JOIN calendar ON trips.service_id = calendar.service_id
	INNER JOIN stops ON stop_times.stop_id = stops.stop_id;

DROP TABLE agency;
DROP TABLE calendar;
DROP TABLE calendar_dates;
DROP TABLE routes;
DROP TABLE shapes;
DROP TABLE stop_times;
DROP TABLE trips;

CREATE INDEX stop_index ON
	stop_lookup(stop_id ASC, arrival_time ASC);

VACUUM;
