#!/usr/bin/python3
# vim : set noexpandtab tabstop=8

import time
import argparse
import sqlite3
import os

db_location = '/users/jy2wong/Code/grt'

parser = argparse.ArgumentParser()
stop = parser.add_mutually_exclusive_group()
stop.add_argument("-s", "--stopid", 
		help="Bus stop's four digit stop id", 
		type=int)
stop.add_argument("-i", "--intersection", 
		help="Bus stop's intersection. Order doesn't matter.", 
		nargs=2, metavar=("STREET_1", "STREET_2"))

parser.add_argument("-t", "--time", 
		help="Display only buses scheduled after TIME. If not \
		specified, defaults to now. If no arguments are given, all \
		matching bus times are displayed. TIME must be of the form \
                HH:MM:SS (e.g. 23:45:01).", 
		const="all", 
		default=time.strftime("%H:%M:%S", time.localtime()), 
		nargs='?')

parser.add_argument("-d", "--day", 
		help="Use the bus schedule for DAY. If not specified, \
		defaults to today. Specify full day of the week, e.g. Monday", 
		const=-1,
		default=-1,
		nargs='?')

parser.add_argument("-n", "--limit", 
		help="Choose how many rows to list. A limit of -1 will cause \
		all rows to be displayed. Defaults to 10.", 
		default=10, type=int)

args = parser.parse_args()

single_stop_id = False
stop_id = -1
limit_str = ""
active_date = 0

if (args.time == "all"):
	args.limit = -1
	args.time = "00:00:00"

if (args.day == -1):
    args.day = time.strftime("%A", time.localtime())
    active_date = int(time.strftime("%Y%m%d", time.localtime()))
else:
    active_date = int(time.strftime("%Y%m%d", time.localtime()))
    # ^ TODO

if (args.limit >= 0):
	limit_str = "LIMIT 0, {}".format(args.limit)

if (args.stopid):
	if (args.stopid >= 0):
		stop_id = args.stopid
		single_stop_id = True
	else:
		print("Stop IDs must be positive.")
		exit()
elif (args.intersection):
	args.intersection[0] = args.intersection[0].title()
	args.intersection[1] = args.intersection[1].title()
else:
	print("You didn't specify a stop ID or an intersection!")
	parser.print_help()
	exit()

# sqlite database
db_path = os.path.join(db_location, 'kwgtfs.db')
if os.path.isfile(db_path):
	conn = sqlite3.connect(db_path)
	c = conn.cursor()
else:
	print("Database doesn't exist at {}.".format(db_path),
			"Did you remember to set db_location?")
	exit()

if (args.intersection):
	c.execute('''SELECT stop_id,stop_name 
			FROM stops WHERE stop_name LIKE ? AND stop_name LIKE ?''', 
			(''.join(['%', args.intersection[0], '%']), 
			 ''.join(['%', args.intersection[1], '%'])) )

	stop_id = c.fetchall()

	if len(stop_id) > 1:
		print("There's more than one stop matching that intersection.")
		print(stop_id)
	elif len(stop_id) == 1:
		stop_id = stop_id[0]
		single_stop_id = True
	else:
		print("No stops found.")
		conn.close()
		exit()

if (single_stop_id):
	print("Stop ID {} after {} on {}".format(stop_id, args.time, args.day))
	c.execute('''
	SELECT arrival_time,
		   stop_name, trip_headsign
	FROM stop_lookup
	WHERE stop_id = {id}
			AND arrival_time >= ?
			AND {day} = 1
			AND start_date <= {date}
			AND end_date >= {date}
	ORDER BY arrival_time
	{limit}
	'''.format(id=stop_id, day=args.day.lower(), limit=limit_str,
		date=active_date), (args.time,))
else:
	print("Showing buses leaving from the above intersections after {} on {}".format(args.time, args.day))
	c.execute('''
		SELECT stop_id, arrival_time,
		       stop_name,trip_headsign
		FROM stop_lookup
		WHERE stop_id IN ({ids})
		  AND arrival_time >= ?
		  AND {day} = 1
		  AND start_date <= {date}
		  AND end_date >= {date}
		ORDER BY arrival_time
		{limit}
		'''.format(day=args.day.lower(), limit=limit_str,
			date=active_date,
			ids=','.join((sid[0] for sid in stop_id))),
		(args.time,))

for row in c:
	print(row)

conn.close()

