import mysql.connector


_db = None


def get_db():
    global _db
    if _db is not None:
        return _db
    _db = Database()
    _db.connect()
    return _db


class Database:
    def __init__(self):
        self.host = 'db'  # Docker container name
        self.user = 'root'
        self.port = '3306'
        self.socket = '/Applications/MAMP/tmp/mysql/mysql.sock'
        self.password = 'root'
        self.database = 'software_engineering'
        self.conn = None
        self.autocommit = True

    def connect(self):
        self.conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            port=self.port,
            # unix_socket=self.socket,
            password=self.password,
            database=self.database
        )

    def close(self):
        if self.conn:
            self.conn.close()

    def execute_select(self, query, values=None):
        cursor = self.conn.cursor()
        cursor.execute(query, values)
        results = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        data = [dict(zip(columns, row)) for row in results]
        cursor.close()
        return data

    def execute_insert(self, query, values):
        cursor = self.conn.cursor()
        cursor.execute(query, values)
        if self.autocommit:
            self.conn.commit()
        last_id = cursor.lastrowid
        cursor.close()
        return last_id

    def execute_update(self, query, values):
        cursor = self.conn.cursor()
        cursor.execute(query, values)
        if self.autocommit:
            self.conn.commit()
        count = cursor.rowcount
        cursor.close()
        return count

    def execute_delete(self, query, values):
        cursor = self.conn.cursor()
        cursor.execute(query, values)
        if self.autocommit:
            self.conn.commit()
        count = cursor.rowcount
        cursor.close()
        return count
