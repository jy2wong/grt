#!/usr/bin/python3
# vim : set noexpandtab tabstop=4

from datetime import datetime,time,timedelta
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
        default=datetime.now().time().strftime("%H:%M:%S"),
        nargs='?')

parser.add_argument("-d", "--day",
        help="Use the bus schedule for DAY. If not specified, \
              defaults to today. Specify full day of the week, e.g. Monday",
        const=None,
        default=None,
        nargs='?')

parser.add_argument("-n", "--limit",
        help="Choose how many rows to list. A limit of -1 will cause \
              all rows to be displayed. Defaults to 10.",
        default=10, type=int)

args = parser.parse_args()

single_stop_id = None
matching_stop_ids = None
sql_limit_str = ""
active_dt = None
active_date = ""

# if no time specified, set time to midnight
if (args.time == "all"):
    args.limit = None
    args.time = "00:00:00"

active_dt = datetime.strptime(args.time, "%H:%M:%S")
active_dt = datetime.combine(datetime.today(), active_dt.timetz())

if (args.day is not None):
    # day specified
    one_day = timedelta(days=1)
    args.day = args.day.capitalize()
    while (args.day not in active_dt.strftime("%A")):
        active_dt = active_dt + one_day
# otherwise, default to today.

args.day = active_dt.strftime("%A")  # e.g. args.day = "Sunday"
active_date = active_dt.strftime("%Y%m%d")  # e.g. active_date = "20140123"

if (args.limit is not None):
    sql_limit_str = "LIMIT 0, {}".format(args.limit)

# set stop_id or canonicalize args.intersection
if (args.stopid):
    if (args.stopid >= 0):
        single_stop_id = args.stopid
    else:
        print("Stop IDs must be positive.")
        exit()
elif (args.intersection):
    args.intersection[0] = args.intersection[0].title()
    args.intersection[1] = args.intersection[1].title()
else:
    print("Please specify a stop ID or an intersection.")
    parser.print_help()
    exit()

# open the sqlite database of GTFS info
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
               ''.join(['%', args.intersection[1], '%'])))

    matching_stop_ids = c.fetchall()

    if len(matching_stop_ids) > 1:
        print("There's more than one stop matching that intersection:")
        print(["{} ({})".format(*s) for s in matching_stop_ids])
    elif len(matching_stop_ids) == 1:
        single_stop_id = matching_stop_ids[0]
    else:
        print("No stops found.")
        conn.close()
        exit()

if (single_stop_id is not None):
    print("Showing schedule for stop ID {} after {} on {}".format(
        single_stop_id, args.time, args.day))
    c.execute('''
    SELECT service_id, arrival_time,
           stop_name, trip_headsign
    FROM stop_lookup
    WHERE stop_id = {id}
            AND arrival_time >= ?
            AND {day} = 1
            AND start_date <= {date}
            AND end_date >= {date}
    ORDER BY arrival_time
    {limit}
    '''.format(id=single_stop_id, day=args.day.lower(), limit=sql_limit_str,
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
        '''.format(day=args.day.lower(), limit=sql_limit_str,
            date=active_date,
            ids=','.join((sid[0] for sid in matching_stop_ids))),
        (args.time,))

# display results of bus schedule query
for row in c:
    print("{thing}  {arrival_time}  [{stop_name}] {trip_headsign}".format(
        thing=row[0], arrival_time=row[1][:5], stop_name=row[2],
        trip_headsign=row[3]))

conn.close()

