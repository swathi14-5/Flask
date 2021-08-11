# Importng Sqlite3 and defining the setup and the connection
import sqlite3


def setup():
    conn = sqlite3.connect('Ecommerce01.db')
    c = conn.cursor()


# Creating a database
    query1 = '''
                CREATE TABLE IF NOT EXISTS customers(
                    cust_id INT NOT NULL PRIMARY KEY,
                    cust_name VARCHAR NOT NULL,
                    username VARCHAR NOT NULL UNIQUE,
                    password VARCHAR NOT NULL,
                    level INT NOT NULL
                );
            '''

    query2 = '''
                    CREATE TABLE IF NOT EXISTS vendors(
                        vendorid INT NULL PRIMARY KEY,
                        cust_id INT NOT NULL NULL REFERENCES customers(cust_id),
                        storename VARCHAR NOT NULL UNIQUE,
                        store_num INT NOT NULL,
                        store_addr VARCHAR NOT NULL
                    );
                '''

    query3 = '''
                    CREATE TABLE IF NOT EXISTS items(
                        itemid PRIMARY KEY NOT NULL,
                        vendorid INT NOT NULL NULL REFERENCES vendors(vendorid),
                        itemname VARCHAR NOT NULL,
                        quantity INT NOT NULL,
                        price REAL NOT NULL
                    );
                '''

    query4 = '''
                    CREATE TABLE IF NOT EXISTS orders(
                        orderid PRIMART KEY NOT NULL,
                        cust_id INT NOT NULL REFERENCES customers(cust_id),
                        itemid INT NOT NULL REFERENCES items(itemid),
                        order_item_name VARCHAR NOT NULL REFERENCES items(itemname),
                        ordered_qty INT NOT NULL,
                        total_amount REAL NOT NULL
                    );
                '''
#Executing the queries
    c.execute(query1)
    c.execute(query2)
    c.execute(query3)
    c.execute(query4)
    
#Commiting the database and closing the connection
    conn.commit()
    conn.close()
