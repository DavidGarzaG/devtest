import sqlite3
import csv


class Database:
    def __init__(self):
        # Here we do things
        self.column_names = {
            "clients" : ["client_id", "first_name", "last_name"],
            "buildings": ["building_id", "client_id", "building_type", "address"],
            "elevator": ["elevator_id", "building_id", "timestamp", "resting_floor", "floor_demanded", "out_or_in_demand", "weight"],
        }

    def insert_data(self, table_name, csv_path=None, *args):
        """
        Generic method to insert data. 
        Supports directly giving the arguments or reading from a csv.
        """

        correct_len = len(self.column_names[table_name])
        values_placeholder = str(tuple('?' for x in range(len(self.column_names[table_name])))).replace("'", "")
        data_to_be_inserted = list()

        if not csv_path:
            try:
                # TODO: Ensure multiple rows at the same time
                assert len(args) == correct_len
            except:
                raise AssertionError(f"The amount of arguments is not equal to the amount of columns for the table {table_name}")

            data_to_be_inserted = [args,]

        else:
            with open(csv_path, mode ='r')as file:
                csvFile = csv.reader(file)
                for lines in csvFile:
                        data_to_be_inserted.append(lines)

        # Open connection
        connection = sqlite3.connect("elevator.db")
        cursor = connection.cursor()

        # Do things
        cursor.executemany(f"""
        INSERT INTO {table_name} {str(tuple(self.column_names[table_name])).replace("'", "")} VALUES {values_placeholder}
        """, data_to_be_inserted)

        # Commit change
        connection.commit()

        # Close connection
        cursor.close()
        connection.close()
