all: data kwgtfs.db

kwgtfs.db: create_kwgtfs.sql
	sqlite3 kwgtfs.db < create_kwgtfs.sql

data: GRT_GTFS.zip
	unzip GRT_GTFS.zip -d data

clean:
	@- rm -f kwgtfs.db
	@- rm -rf data/
