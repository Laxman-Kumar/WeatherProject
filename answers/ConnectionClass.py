import psycopg2

class PostgreConnection:

    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password= password
        self.conn = None
    
    def connect(self):
        try:
        # read connection parameters

        # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            self.conn = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)
            return self.conn
        
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    

    def close(self):
        if self.conn is not None:
            self.conn.close()
            print('Database connection closed.')