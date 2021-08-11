# Importing flask and the required methods

from flask import Flask, request, jsonify
import Model


app = Flask(__name__)

session = dict()

# Creating all the required routes

@app.route("/Ecommerce/")
def doc():
    return "<b>This is an Ecommerce website</b>"

# Add customer New customer can be added
@app.route("/Ecommerce/add_Customer",methods=["POST","GET"])
def add_Customer():
    #if session.get('username',None):
        param = request.get_json()
        result=Model.add_customer(param)
        return jsonify(result)
    #return jsonify({"msg": "Login first!", "status": 403})

# This is for Login - takes username and password of signed up users and validates them
@app.route("/Ecommerce/login",methods=["POST","GET"])
def login():
    if not session.get('username', None):
        param = request.get_json()
        result,msg=Model.login(param)
        if result:
            session['username'] = param["username"]
        return jsonify(msg)
    return jsonify({"msg": "Already logged-in!", "status": 400})


#Creating the vendor - only vendors can store the details
@app.route("/Ecommerce/add_Vendor",methods=["POST","GET"])
def add_Vendor():
    if session.get('username', None):
        param = request.get_json()
        result=Model.add_vendor(session.get('username', None), param)
        return jsonify(result)
    return jsonify({"msg": "Login first!", "status": 403})


# Creating add_items URI - vendor can add item details  
@app.route("/Ecommerce/add_items",methods=["POST","GET"])
def add_items():
    if session.get('username', None):
        if Model.get_level(session.get('username', None)) == 1:
            param = request.get_json()
            result=Model.add_item(session.get('username', None), param)
            return jsonify(result)
        return jsonify({"msg": "Only a vendor can add products", "status": 403})
    return jsonify({"msg": "Login first!", "status": 403})


# Here comes the Search_Item_by_name URI - any loggedin cutsomer or vendor can call this API
@app.route("/Ecommerce/Search_item_by_name",methods=["POST","GET"])
def Search_item_by_name():
    if session.get('username', None):
        param = request.get_json()
        result=Model.search_by_item(param)
        return jsonify(result)
    return jsonify({"msg": "Login first!", "status": 403})

# Place_order route and input & output parameters should be in "JSON"
@app.route("/Ecommerce/Place_order",methods=["POST","GET"])
def Place_order():
    if session.get('username', None):
        param = request.get_json()
        quantity = Model.get_quantity(param["itemname"])
        if len(quantity) > 1:
            return jsonify({"msg": f"there are more than one item with name {param['itemname']}", "status": 400})
        elif len(quantity) == 0:
            return jsonify({"msg": f"there is no item with name {param['itemname']}", "status": 400})
        else:
            print(quantity)
            quantity = quantity[0][0]
            if quantity:
                if quantity > 0:
                    result=Model.place_order(session.get('username', None), param)
                    return jsonify(result)
                return jsonify({"msg": "Out of stock!", "status": 400})
            return jsonify({"msg": "enter a valid item name", "status": 400})
    return jsonify({"msg": "Login first!", "status": 403})


# Get_all_orders_for_customer - Only logged in user can call this API.   
@app.route("/Ecommerce/Get_all_orders_by_customer",methods=["POST","GET"])
def Get_all_orders_by_customer():
    if session.get('username', None):
        param = request.get_json()
        result=Model.get_all_orders_by_customer(param["custid"])
        return jsonify(result)
    return jsonify({"msg": "Login first!", "status": 403})


# GET orders - Only admins can call this API. This API returns all the orders in the orders table 
@app.route("/Ecommerce/Get_all_orders",methods=["POST","GET"])
def Get_all_orders():
    print(session.get('username'))
    if not session.get('username' ) == None:
        param = request.get_json()
        result=Model.get_All_Orders()
        return jsonify(result)
    return jsonify({"msg": "Login first!", "status": 403})


# GET all vendors - Only admins can call this API. This API returns all the orders in the orders table 
@app.route("/Ecommerce/Get_all_vendors",methods=["POST","GET"])
def Get_all_vendors():
    if not session.get('username') ==  None:
        param = request.get_json()
        result=Model.get_All_Vendors()
        return jsonify(result)
    return jsonify({"msg": "Login first!", "status": 403})

# This route gives logout
@app.route("/Ecommerce/Logout",methods=["POST","GET"])
def Logout():
    if session.get('username', None):
        session.pop('username', None)
        return jsonify({"msg": "Logout successful!", "status": 200})
    return jsonify({"msg": "Login first!", "status": 403})


if __name__ == '__main__':
    app.run(debug=True)
