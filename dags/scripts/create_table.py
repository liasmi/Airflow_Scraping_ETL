from sqlalchemy import create_engine

def create_table_sql():
    username = "store"
    password = "store" 
    ipaddress = "db"
    port = 3306
    dbname = "books" 
    mysql_str = f'mysql://{username}:{password}@{ipaddress}:{port}/{dbname}'
    cnx = create_engine(mysql_str)
    cnx.execute('''
    CREATE TABLE IF NOT EXISTS users (
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL,
                country TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                email VARCHAR(200) NOT NULL PRIMARY KEY
            );
    ''')
