import unittest
from datetime import datetime
import sqlite3
from main import Database
import csv
import tempfile
import os

class TestMain(unittest.TestCase):

    def test_clients_column_names(self):
        
        connection = sqlite3.connect("elevator.db")
        cursor = connection.execute(f'select * from clients')
        names = [description[0] for description in cursor.description]

        assert names == ["client_id", "first_name", "last_name"]
        
        cursor.close()
        connection.close()

    def test_buildings_column_names(self):
        
        connection = sqlite3.connect("elevator.db")
        cursor = connection.execute(f'select * from buildings')
        names = [description[0] for description in cursor.description]

        assert names == ["building_id", "client_id", "building_type", "address"]
        
        cursor.close()
        connection.close()

    def test_elevator_column_names(self):
        
        connection = sqlite3.connect("elevator.db")
        cursor = connection.execute(f'select * from elevator')
        names = [description[0] for description in cursor.description]

        assert names == ["elevator_id", "building_id", "timestamp", "resting_floor", "floor_demanded", "out_or_in_demand", "weight"]
        
        cursor.close()
        connection.close()

    def test_inserting_client_through_args(self):
        test_input = [100, "John", "Doe"]
        
        db = Database()
        db.insert_data("clients", None, *test_input)

        # Open connection
        connection = sqlite3.connect("elevator.db")
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM clients ORDER BY client_id DESC LIMIT 1;")

        last_input = [x for x in cursor][0]

        assert last_input == tuple(test_input)

        # Deleting the test.
        cursor.execute("DELETE FROM clients WHERE client_id = (SELECT MAX(client_id) FROM clients)")
        connection.commit()

        # Close connection
        cursor.close()
        connection.close()


    def test_inserting_building_through_args(self):
        test_input = [100000, 0, "apartment", "7306GartnerAve.NewYork"]
        
        db = Database()
        db.insert_data("buildings", None, *test_input)

        # Open connection
        connection = sqlite3.connect("elevator.db")
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM buildings ORDER BY building_id DESC LIMIT 1;")

        last_input = [x for x in cursor][0]

        assert last_input == tuple(test_input)

        # Deleting the test.
        cursor.execute("DELETE FROM buildings WHERE building_id = (SELECT MAX(building_id) FROM buildings)")
        connection.commit()

        # Close connection
        cursor.close()
        connection.close()

    def test_inserting_elevator_through_args(self):

        # This timestamp is for 2054/01/01
        test_input = [1000,0, 2650860000, 0, 1, 1, 85.6]
        
        db = Database()
        db.insert_data("elevator", None, *test_input)

        # Open connection
        connection = sqlite3.connect("elevator.db")
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM elevator ORDER BY timestamp DESC LIMIT 1;")

        last_input = [x for x in cursor][0]

        assert last_input == tuple(test_input)

        # Deleting the test.
        cursor.execute("DELETE FROM elevator WHERE timestamp = (SELECT MAX(timestamp) FROM elevator)")
        connection.commit()

        # Close connection
        cursor.close()
        connection.close()

    def test_inserting_clients_through_csv(self):
        """
        """
        clients_data = [
            [10002,"David","Garza"],
            [10001,"Mary","Jane"],
            [10000,"John","Doe"],
        ]

        tf = tempfile.NamedTemporaryFile(delete=False)

        with open(tf.name, "w", newline="") as temp_csv_file:
            csv_writer = csv.writer(temp_csv_file)
            csv_writer.writerows(clients_data)

        db = Database()
        db.insert_data("clients", csv_path=tf.name)

        # Closing temp file
        tf.close()
        os.unlink(tf.name)

        connection = sqlite3.connect("elevator.db")
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM clients ORDER BY client_id DESC LIMIT 3;")

        last_input = [x for x in cursor]

        assert last_input == [tuple(x) for x in clients_data]

        # Deleting the biggest three records.
        for _ in range(3):
            cursor.execute("DELETE FROM clients WHERE client_id = (SELECT MAX(client_id) FROM clients)")
        
        connection.commit()

        # Close connection
        cursor.close()
        connection.close()


    def test_inserting_buildings_through_csv(self):
        """
        """
        buildings_data = [
            [100004,2,"apartment","768AlderwoodSt.NewYork"],
            [100003,1,"apartment","570HilltopRoadJacksonHeights"],
            [100002,1,"apartment","384BlackburnSt.Brooklyn"],
            [100001,0,"apartment","692BridgeAvenueNewburgh"],
            [100000,0,"apartment","7306GartnerAve.NewYork"],
        ]

        tf = tempfile.NamedTemporaryFile(delete=False)

        with open(tf.name, "w", newline="") as temp_csv_file:
            csv_writer = csv.writer(temp_csv_file)
            csv_writer.writerows(buildings_data)

        db = Database()
        db.insert_data("buildings", csv_path=tf.name)

        # Closing temp file
        tf.close()
        os.unlink(tf.name)

        connection = sqlite3.connect("elevator.db")
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM buildings ORDER BY building_id DESC LIMIT 5;")

        last_input = [x for x in cursor]

        assert last_input == [tuple(x) for x in buildings_data]

        # Deleting the biggest three records.
        for _ in range(5):
            cursor.execute("DELETE FROM buildings WHERE building_id = (SELECT MAX(building_id) FROM buildings)")
        
        connection.commit()

        # Close connection
        cursor.close()
        connection.close()

    def test_inserting_elevator_through_csv(self):
        """
        """
        elevator_data = [
            [0,0,2650860002,0,1,1,85.6],
            [0,0,2650860001,1,0,1,85.6],
            [0,0,2650860000,0,1,1,85.6],
        ]

        tf = tempfile.NamedTemporaryFile(delete=False)

        with open(tf.name, "w", newline="") as temp_csv_file:
            csv_writer = csv.writer(temp_csv_file)
            csv_writer.writerows(elevator_data)

        db = Database()
        db.insert_data("elevator", csv_path=tf.name)

        # Closing temp file
        tf.close()
        os.unlink(tf.name)

        connection = sqlite3.connect("elevator.db")
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM elevator ORDER BY timestamp DESC LIMIT 3;")

        last_input = [x for x in cursor]

        assert last_input == [tuple(x) for x in elevator_data]

        # Deleting the biggest three records.
        for _ in range(3):
            cursor.execute("DELETE FROM elevator WHERE timestamp = (SELECT MAX(timestamp) FROM elevator)")
        
        connection.commit()

        # Close connection
        cursor.close()
        connection.close()


