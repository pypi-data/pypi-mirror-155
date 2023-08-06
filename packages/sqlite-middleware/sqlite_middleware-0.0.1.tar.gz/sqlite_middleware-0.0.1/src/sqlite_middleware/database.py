import sqlite3

class Db():
    """Class to create sqlite connection, and provide usefull methods to manage this data.
    database : str -> name of sqlite file"""
    def __init__(self, database) -> None:
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def __del__(self):
        # When object is deleted, close connection to database.
        try:
            self.cursor.close()
            self.connection.close()
        except sqlite3.ProgrammingError:
            pass

    
    def select_all(self, cls):
        # Give a class to this function, and it will retrieve all objects with this class from the database
        table_name = f"tbl{cls.__name__}s"

        sql = f"SELECT * FROM {table_name}"

        all_rows = self.cursor.execute(sql).fetchall()
        
        return all_rows

    
    def select_by_id(self, cls, id):
        # Give a class and an id to this function, and it will retrieve the object with this id from the database
        table_name = f"tbl{cls.__name__}s"

        sql = f"SELECT * FROM {table_name} WHERE id={id}"

        all_rows = self.cursor.execute(sql).fetchall()
        
        return all_rows    


    def create_table(self, object):
        # Give an object class to this function, and a new table for this class will be created
        table_name = f"tbl{object.__class__.__name__}s"
        dict = object.__dict__

        sql = f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY, "

        for key in dict:
            sql += f"'{key}'"
            if key != list(dict)[-1]:
                sql += ", "

        sql += ") "

        self.cursor.execute(sql)
        self.connection.commit()


    def save_object(self, object):
        # Give an object to this function, and it will be saved in the sqlite database
        dict = object.__dict__

        sql = f"INSERT INTO tbl{object.__class__.__name__}s ("

        for key in dict:
            sql += f"'{key}'"
            if key != list(dict)[-1]:
                sql += ", "

        sql += ") VALUES("

        for key in dict:
            sql += f"'{dict[key]}'"
            if key != list(dict)[-1]:
                sql += ", "
        sql += ")"

        self.create_table(object) # Make sure table exists before saving object

        self.cursor.execute(sql)
        self.connection.commit()


    def update_object(self, id, object):
        # Give an object to this function, and it will be updated in sqlite
        dict = object.__dict__
        table_name = f"tbl{object.__class__.__name__}s"

        sql = f"UPDATE {table_name} SET "

        for key in dict:
            sql += f"'{key}' = '{dict[key]}'"
            if key != list(dict)[-1]:
                sql += ", "
        
        sql += f"WHERE id={id}"

        self.cursor.execute(sql)
        self.connection.commit()

    
    def delete_object(self, cls, id):
        # Give a class and an id to this function, and it will delete the object with this id from the database
        table_name = f"tbl{cls.__name__}s"

        sql = f"DELETE FROM {table_name} WHERE id={id}"

        self.cursor.execute(sql)
        self.connection.commit()
