import sqlite3

DB_FOLDER = 'db/'

class DB:
    def dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def __init__(self, db_name, check_same_thread=True):
        self.conn = sqlite3.connect(DB_FOLDER + db_name + '.db' , check_same_thread=check_same_thread)
        self.conn.row_factory = self.dict_factory
        self.cursor = self.conn.cursor()

    def query(self, sql, params=None):
        if params:
            self.cursor.execute(sql, params)
        else:
            self.cursor.execute(sql)
        return self.cursor.fetchall()

    def __del__(self):
        self.conn.close()