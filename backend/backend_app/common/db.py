"""
Database Operations Class
"""


class SqliteDBMS:

    def __init__(self, db_dir):
        """
        SQLite dbms class
        @param db_dir: database directory
        """
        self.conn = None
        self.cursor = None
        pass

    def add(self, table, col_to_val):
        """
        @param table: name of table
        @param col_to_val:  dict of column name to value
        @return: <boolean> success
        """
        cols_str = str(tuple(col_to_val.keys())).replace("'", '')
        vals_str = str(tuple(col_to_val.values()))
        sql = """INSERT INTO {} {} VALUES {}""".format(table, cols_str, vals_str)
        # print('sql: ', sql)
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            return True
        except Exception:
            self.conn.rollback()
            print('error when adding to db')
            print(Exception)
            return False
        pass

    def close(self):
        """
        Close the database
        """
        self.conn.commit()
        self.conn.close()

    def delete(self, index):
        """
        @param index: index to delete
        @return: <boolean> success
        """
        pass

    def query(self, query_str):
        """
        @param query_str: <str> sql query
        @return: <boolean> success
                 <dict> result
        """
        try:
            self.cursor.execute(query_str)
            return True, self.cursor.fetchall()
        except:
            return False, None
        pass

    def update(self, db_index, col_to_val=None):
        """
        @param db_index: index of row
        @param col_to_val: dict of column name to new value
        @return: <boolean> success
        """

        if col_to_val is None:
            col_to_val = {}
        pass
