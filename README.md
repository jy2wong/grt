grt.py
======
By Jenny Wong

About
-----

grt.py is a little python script that gives information about when
certain Grand River Transit buses leave from certain stops around the
Kitchener-Waterloo area. 

It exists mostly because I wanted to make sure I still remembered how
to write things in python.

Contains information provided by the Regional Municipality of Waterloo
under licence.

The current GRT_GTFS.zip provided in this repository contains data that
is valid from September 2 2014 to April 26 2015.
I'll try to keep the GRT_GTFS.zip up to date (I actually use this thing
sort of frequently), but if it's not, you can download your own copy of
the GTFS data.

The latest GTFS data can be found here:
http://www.regionofwaterloo.ca/en/regionalGovernment/GRT_GTFSdata.asp

Installation
------------

grt.py uses python3 and sqlite3, and you'll need to make sure both are
installed before you can use grt.py.

To generate the database, use

	make all

Don't forget to change db_location in grt.py before you use the script!

Usage
-----
	usage: grt.py [-h] [-s STOPID | -i STREET_1 STREET_2] [-t [TIME]] [-d [DAY]]
				  [-n LIMIT]

	optional arguments:
	  -h, --help            show this help message and exit
	  -s STOPID, --stopid STOPID
							Bus stop's four digit stop id
	  -i STREET_1 STREET_2, --intersection STREET_1 STREET_2
							Bus stop's intersection. Order doesn't matter.
	  -t [TIME], --time [TIME]
							Display only buses scheduled after TIME. If not
							specified, defaults to now. If no arguments are given,
							all matching bus times are displayed. TIME must be of
							the form HH:MM:SS (e.g. 23:45:01).
	  -d [DAY], --day [DAY]
							Use the bus schedule for DAY. If not specified,
							defaults to today. Specify full day of the week, e.g.
							Monday
	  -n LIMIT, --limit LIMIT
							Choose how many rows to list. A limit of -1 will cause
							all rows to be displayed. Defaults to 10.

Examples
--------

If you know the 4-digit stop id, you can use grt.py just like you would
the texting service.

	grt.py -s 2014

But if you don't, you can try going by intersection instead.
You don't need to type entire street names, and neither order nor case
matter. The following all result in the same query:

	grt.py -i university westmount
	grt.py -i uni west
	grt.py -i west uni

This is a neat trick you can use to display most buses leaving from 
Ring Road.

	grt.py -i 'u.w.' ''

Caveats
-------

grt.py currently only understands holidays when the --day flag is not
being used. GRT buses are on holiday
schedule (i.e. Sunday schedule) on the days listed here:
http://www.grt.ca/en/routesschedules/holidayservice.asp
