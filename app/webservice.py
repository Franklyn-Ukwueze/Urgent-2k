from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from app import wallets
from app.helpers import get_balance

# creating the flask app
app = Flask(__name__)
# creating an API object
api = Api(app)

class Home(Resource):
    def get(self):
        return {'message': "Welcome to the homepage of this webservice."}
api.add_resource(Home,'/')

class Balance(Resource):
    def get(self, userphone):
        if userphone.isdigit() and len(userphone) == 11:
            data = wallets.find_one({"userphone": userphone})
            if data:
                print(f"'balance': {data['balance']}")
                return {"balance": data["balance"]} 
            else:
                return None
        else:
            return None
api.add_resource(Balance, "/balance/<string:userphone>")

class Credit(Resource):
    def post(self, userphone, amount):
        if userphone.isdigit() and len(userphone) == 11:
            if amount.isdigit(): 
                amount = round(float(amount), 2)
                if amount > 0:
                    amount = round(float(amount), 2)
                    if get_balance(userphone):
                        old_balance = get_balance(userphone)
                        new_balance = old_balance + amount
                        wallets.update_one({"userphone": userphone}, {"$set": {"balance": new_balance}})
                        
                    else:
                        return None
                else:
                    return None
            else:
                return None
        else:
            return None
api.add_resource(Credit, "/credit/<string:userphone>/<string:amount>")

class Debit(Resource):
    def post(self, userphone, amount):
        if userphone.isdigit() and len(userphone) == 11:
            if amount.isdigit:
                amount = round(float(amount), 2) 
                if amount > 0:
                    if get_balance(userphone):
                        old_balance = get_balance(userphone)
                        if old_balance - amount > 100.00:
                            new_balance = old_balance - amount
                            wallets.update_one({"userphone": userphone}, {"$set": {"balance": new_balance}})
                        else:
                            return None
                    else:
                        return None
                else:
                    return None
            else:
                return None
        else:
            return None
api.add_resource(Debit, "/credit/<string:userphone>/<string:amount>")
