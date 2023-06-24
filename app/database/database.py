import mysql.connector


class Database:
    def __init__(self, host, port, socket, user, password, database):
        self.host = host
        self.user = user
        self.port = port
        self.socket = socket
        self.password = password
        self.database = database
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            port=self.port,
            unix_socket=self.socket,
            password=self.password,
            database=self.database
        )
        self.cursor = self.conn.cursor()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def execute_query(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def execute_insert(self, query, values):
        self.cursor.execute(query, values)
        self.conn.commit()
        last_id = self.cursor.lastrowid
        return last_id
