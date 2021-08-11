#Importing sqlite3 & database.py file

import sqlite3
import database

# Add customer New customer can be added
def add_customer(param):
    setup()
    conn = sqlite3.connect("Ecommerce01.db")
    c = conn.cursor()
    custid = get_max_custid()
    sqlquery = f'''
                    INSERT INTO customers VALUES({custid},'{param["name"]}','{param["username"]}','{param["password"]}',{param["level"]});
            '''
    try:
        c.execute(sqlquery)
    except Exception as e:
        return {"msg": str(e), "status": 403}
    else:
        conn.commit()
        return {"msg": "Registration successfully", "status": 201}
    finally:
        conn.close()


# Creating add_items URI - vendor can add item details 
def add_item(username, param):
    setup()
    conn = sqlite3.connect("Ecommerce01.db")
    c = conn.cursor()
    itemid = get_max_itemid()
    vendorid = get_vendorid(get_custid(username)) + 1
    sqlquery = f'''
                    INSERT INTO items(itemid, vendorid, itemname, quantity, price)
                    VALUES({itemid},{vendorid},'{param["itemname"]}',{param["quantity"]},{param["price"]});
                '''
    try:
        c.execute(sqlquery)
        conn.commit()
    except Exception as e:
        return {"msg": str(e), "status": 400}
    else:
        itemid += 1
        conn.commit()
        return {"msg": "Product added Successfully", "status": 201}
    finally:
        conn.close()

# This is for Login - takes username and password of signed up users and validates them
def login(param):
    setup()
    conn = sqlite3.connect("Ecommerce01.db")
    c = conn.cursor()
    query = f'''
                SELECT * FROM customers WHERE username='{param["username"]}' and password='{param["password"]}';
            '''
    try:
        result = c.execute(query).fetchall()
    except Exception as e:
        conn.close()
        return False, {"msg": str(e), "status": 400}
    if len(result) > 0:
        return True, {"msg": "login Successful!", "status": 200}
    return False, {"msg": "Incorrect username or password!", "status": 400}

#Creating the vendor - only vendors can store the details
def add_vendor(username, param):
    setup()
    conn = sqlite3.connect("Ecommerce01.db")
    c = conn.cursor()
    vendorid = get_max_vendorid()
    custid = get_custid(username)
    if not custid:
        return {"msg": "Register as a customer first!", "status": 400}
    print(vendorid)
    print(custid)
    query = f'''
                INSERT INTO vendors(vendorid, cust_id, storename, store_num, store_addr)
                VALUES({vendorid}, {custid}, '{param["storename"]}', {param["store_num"]}, '{param["store_addr"]}');
            '''
    try:
        c.execute(query)
        conn.commit()
    except Exception as e:
        print("test1")
        return {"msg": str(e), "status": 400}

    query_update = f'''
                    UPDATE customers
                    SET level=1
                    WHERE cust_id={custid};
                '''
    try:
        c.execute(query_update)
        conn.commit()
    except Exception as e:
        print("test1")
        return {"msg": str(e), "status": 400}
    else:
        return {"msg": "Vendor registered", "status": 400}
    finally:
        conn.close()

# Here comes the Search_Item_by_name URI - any loggedin cutsomer or vendor can call this API
def search_by_item(param):
    setup()
    conn = sqlite3.connect("Ecommerce01.db")
    c = conn.cursor()
    query = f'''
                SELECT * FROM items WHERE itemname LIKE '%{str(param["itemname"])}%';
            '''
    try:
        items = c.execute(query).fetchall()
    except Exception as e:
        conn.close()
        return {"msg": str(e), "status": 400}
    print(items)
    if len(items) == 1:
        item = {"item_name": items[0][2], "quantity": items[0][3], "price": items[0][4]}
        return {"data": item, "msg": "success", "status": 200}
    elif len(items) > 1:
        temp = dict()
        for num, item in enumerate(items):
            temp[num] = {"item_name": item[2], "quantity": item[3], "price": item[4]}
        return {"data": temp, "msg": "success", "status": 200}
    else:
        return {"msg": f"No item found with name {param['itemname']}", "status": 200}

# Place_order route and input & output parameters should be in "JSON"
def place_order(username, param):
    setup()
    conn = sqlite3.connect("Ecommerce01.db")
    c = conn.cursor()
    query = f'''
                SELECT itemid, itemname, quantity, price FROM items WHERE itemname LIKE '%{str(param["itemname"])}%';
            '''
    try:
        result = c.execute(query).fetchall()
    except Exception as e:
        conn.close()
        return {"msg": str(e), "status": 400}
    if len(result) > 1:
        return {"msg": f"There are more than one item with name {param['itemname']}", "status": 400}
    elif len(result) == 1:
        itemid = result[0][0]
        itemname = result[0][1]
        quantity = result[0][2]
        price = result[0][3]
    else:
        return {"msg": f"There no items with name {param['itemname']}", "status": 400}
    if quantity < int(param["quantity"]):
        return {"msg": f"Available quantity: {quantity}", "status": 400}
    custid = get_custid(username)
    if not custid:
        return {"msg": "Register as a customer first!", "status": 400}
    orderid = get_max_orderid()
    amount = float(param["quantity"])*float(price)
    query_insert = f'''
                        INSERT INTO orders(orderid, cust_id, itemid, order_item_name, ordered_qty, total_amount)
                        VALUES({orderid},{custid},{itemid},'{itemname}', {param["quantity"]}, {amount});
                    '''
    try:
        c.execute(query_insert)
        conn.commit()
    except Exception as e:
        conn.close()
        return {"msg": str(e), "status": 400}
    new_quantity = int(quantity) - int(param["quantity"])
    query_update = f'''
                        UPDATE items
                        SET quantity={new_quantity}
                        WHERE itemid={itemid};
                    '''
    try:
        c.execute(query_update)
        conn.commit()
    except Exception as e:
        return {"msg": str(e), "status": 400}
    else:
        return {"msg": "Order placed Successfully!", "status": 200}

#Getting level from customers
def get_level(username):
    setup()
    conn = sqlite3.connect("Ecommerce01.db")
    c = conn.cursor()
    query1 = f'''
                    SELECT level FROM customers WHERE username='{username}';
                '''
    try:
        level = c.execute(query1).fetchone()[0]
    except Exception as e:
        return {"msg": str(e), "status": 400}
    else:
        return int(level)

#Getting max item id
def get_max_itemid():
    setup()
    conn = sqlite3.connect("Ecommerce01.db")
    c = conn.cursor()
    query = '''
                    SELECT MAX(itemid) FROM items;
                '''
    try:
        itemid = c.execute(query).fetchone()[0]
        itemid += 1
    except:
        itemid = 30001

    return int(itemid)

#Getting max vendor id
def get_max_vendorid():
    setup()
    conn = sqlite3.connect("Ecommerce01.db")
    c = conn.cursor()
    query = '''
                SELECT MAX(vendorid) FROM vendors;
            '''
    try:
        vendorid = c.execute(query).fetchone()[0]
        vendorid += 1
    except:
        vendorid = 20001

    return int(vendorid)

#Getting max order id
def get_max_orderid():
    setup()
    conn = sqlite3.connect("Ecommerce01.db")
    c = conn.cursor()
    query = '''
                SELECT MAX(orderid) FROM orders;
            '''
    try:
        orderid = c.execute(query).fetchone()[0]
        orderid += 1
    except:
        orderid = 40001

    return int(orderid)


def get_max_custid():
    setup()
    conn = sqlite3.connect("Ecommerce01.db")
    c = conn.cursor()
    query = '''
                    SELECT MAX(cust_id) FROM customers;
                '''
    try:
        custid = c.execute(query).fetchone()[0]
        custid += 1
    except:
        custid = 30001

    return int(custid)

# Getting customer id
def get_custid(username):
    setup()
    conn = sqlite3.connect("Ecommerce01.db")
    c = conn.cursor()
    query = f'''
                    SELECT cust_id FROM customers WHERE username='{username}';
                '''
    try:
        custid = c.execute(query).fetchone()[0]
    except:
        custid = None

    return custid

#Getting vendor id
def get_vendorid(custid):
    setup()
    conn = sqlite3.connect("Ecommerce01.db")
    c = conn.cursor()
    query = f'''
                    SELECT vendorid FROM vendors WHERE cust_id='{custid}';
                '''
    try:
        vendorid = c.execute(query).fetchone()[0]
    except:
        vendorid = None

    return vendorid

def get_quantity(itemname):
    setup()
    conn = sqlite3.connect("Ecommerce01.db")
    c = conn.cursor()
    query = f'''
                SELECT quantity FROM items WHERE itemname LIKE '%{str(itemname)}%';
            '''
    try:
        quantity = c.execute(query).fetchall()
    except:
        quantity = None
    finally:
        conn.close()

    return quantity

def get_All_Vendors():

    conn = sqlite3.connect("Ecommerce01.db")
    c = conn.cursor()
    query = f'''
                SELECT cust_name, storename, store_addr  FROM customers
                INNER JOIN vendors
                on customers.cust_id =  vendors.cust_id
            '''
    try:
        quantity = c.execute(query).fetchall()
    except:
        quantity = None
    finally:
        conn.close()

    return quantity

# Get_all_orders_for_customer - Only logged in user can call this API. 
def get_all_orders_by_customer(custid):
    conn = sqlite3.connect("Ecommerce01.db")
    c = conn.cursor()
    query = f'''
               SELECT * FROM orders where cust_id  = '{str(custid)}' ;
            '''
    try:
        quantity = c.execute(query).fetchall()
    except:
        quantity = None
    finally:
        conn.close()

    return quantity


# GET orders - Only admins can call this API. This API returns all the orders in the orders table 
def get_All_Orders():
    conn = sqlite3.connect("Ecommerce01.db")
    c = conn.cursor()
    query = f'''
               SELECT * FROM orders  ;
            '''
    try:
        quantity = c.execute(query).fetchall()
    except:
        quantity = None
    finally:
        conn.close()

    return quantity

