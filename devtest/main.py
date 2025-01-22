import sqlite3


# Define connection and cursor
connection = sqlite3.connect("elevator.db")

cursor = connection.cursor()

# This new table would be to expand the case to more cases
command1 = """ CREATE TABLE IF NOT EXISTS
clients(client_id INTEGER PRIMARY KEY, first_name TINYTEXT, last_name TINYTEXT)
"""
cursor.execute(command1)

# We could also use the type of building and have different models according to the type of building.
# Comment: Could divide adress into several subsets, but that is beyond the point.
command2 = """ CREATE TABLE IF NOT EXISTS
buildings(building_id INTEGER PRIMARY KEY, building_type TINYTEXT, address TEXT,
FORIEGN KEY(client_id) REFERENCES clients(client_id)) 
"""
cursor.execute(command2)


# This table (without the foreign keys) would be sufficient to store the data that we need for one case
command3 = """ CREATE TABLE IF NOT EXISTS
elevator(elevator_id INTEGER PRIMARY KEY, timestamp DATETIME, resting_floor INTEGER, floor_demanded INTEGER, out_or_in_demand BOOLEAN, weight FLOAT,
FORIEGN KEY(building_id) REFERENCES buildings(building_id)
"""

cursor.execute(command3)


