import random
from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from app.helpers import get_balance, credit, debit, urgent2k_token_required, voucherdb

# creating the flask app
app = Flask(__name__)
# creating an API object
api = Api(app)

class Home(Resource):
    @urgent2k_token_required
    def get(self):
        return {'message': "Welcome to the homepage of this webservice."}
api.add_resource(Home,'/')

# class Balance(Resource):
#     def get(self, userphone):
#         if userphone.isdigit() and len(userphone) == 11:
#             data = wallets.find_one({"userphone": userphone})
#             if data:
#                 return {"Status": True, "message": "Balance successfully retrieved", "data": data.get("balance")}, 200
#             else:
#                 return {"status": False, "message": "User does not exist in database","data": None}, 400
#         else:
#             return {"status": False, "message": "invalid phone number", "data": None}, 400
# api.add_resource(Balance, "/balance/<string:userphone>")

# class Credit(Resource):
#     def post(self, userphone, amount):
#         if userphone.isdigit() and len(userphone) == 11:
#             if amount.isdigit(): 
#                 amount = round(float(amount), 2)
#                 if amount > 0:
#                     amount = round(float(amount), 2)
#                     if get_balance(userphone):
#                         old_balance = get_balance(userphone)
#                         new_balance = old_balance + amount
#                         wallets.update_one({"userphone": userphone}, {"$set": {"balance": new_balance}})
#                         return {"status": True, "message":"User's wallet has been successfully credited", "data": None}, 200
#                     else:
#                         return {"status": False, "message": "User does not exist in database", "data": None}, 400
#                 else:
#                     return {"status": False, "message":"amount is less than 0", "data": None}, 400
#             else:
#                 return {"status": False, "message":"invalid amount", "data": None}, 400
#         else:
#             return {"status": False, "message":"invalid phone number", "data": None}, 400
# api.add_resource(Credit, "/credit/<string:userphone>/<string:amount>")

# class Debit(Resource):
#     def post(self, userphone, amount):
#         if userphone.isdigit() and len(userphone) == 11:
#             if amount.isdigit:
#                 amount = round(float(amount), 2) 
#                 if amount > 0:
#                     if get_balance(userphone):
#                         old_balance = get_balance(userphone)
#                         if old_balance - amount > 100.00:
#                             new_balance = old_balance - amount
#                             wallets.update_one({"userphone": userphone}, {"$set": {"balance": new_balance}})
#                             return {"status": True, "message":"User's wallet has been credited successfully", "data": None}, 200
#                         else:
#                             return {"status": False, "message":"User's balance is too low to be debited", "data": None}, 400
#                     else:
#                         return {"status": False, "message":"User does not exist in database", "data": None}, 400
#                 else:
#                     return {"status": False, "message":"amount is less than 0", "data": None}, 400
#             else:
#                 return {"status": False, "message":"invalid amount", "data": None}, 400
#         else:
#             return {"status": False, "message":"invalid phone number", "data": None}, 400
# api.add_resource(Debit, "/credit/<string:userphone>/<string:amount>")

class CreateVoucher(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('amount', 
                    type=str,
                    required=True,
                    help="Enter Amount and field cannot be left blank")
    
    @urgent2k_token_required
    def get(self, userphone):
        payload = CashVoucher.parser.parse_args()
        amount = payload["amount"]
        if userphone.isdigit() and len(userphone) == 11:
            if amount.isdigit():
                amount = float(amount)
                if amount > 0:
                    balance = float(get_balance(userphone))
                    if balance - amount > 100.0:
                        token = str(random.randint(100000000000, 999999999999))
                        data = voucherdb.find_one({"token": token})
                        while data:
                            token = random.randint(100000000000, 999999999999)
                        debit(userphone, str(amount), token)
                        voucherdb.insert_one({"token": token, "creator": userphone, "amount": amount, "status": "available", "casherphone": "null"})
                        return {"status": True, "message":"voucher has been created successfully", "data": data.get("token") }, 200
                    else:
                        return {"status": False, "message":"insuffient balance.", "data": None}, 400
                else:
                    return {"status": False, "message":"amount is less than 0.", "data": None}, 400
            else:
                return {"status": False, "message":"invalid amount", "data": None}, 400
        else:
            return {"status": False, "message":"invalid phone number", "data": None}, 400
api.add_resource(CreateVoucher, "/createvoucher/<string:userphone>")

class CashVoucher(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('amount', 
                    type=str,
                    required=True,
                    help="Enter Amount and field cannot be left blank")
    parser.add_argument('token', 
                    type=str,
                    required=True,
                    help="Enter token and field cannot be left blank")
    
    @urgent2k_token_required
    def get(self, userphone):
        payload = CashVoucher.parser.parse_args()
        amount = payload["amount"]
        token = payload["token"]
        if userphone.isdigit() and len(userphone) == 11:
            if token.isdigit() and len(token) == 12:
                data = voucherdb.find_one({"token": token})
                if data:
                    if data["status"] == "available":
                        voucherdb.update_one({"token": token}, {"$set": {"status": "cashed"}})
                        voucherdb.update_one({"token": token}, {"$set": {"casherphone": userphone}})
                        amount = data.get("amount")
                        credit(userphone,amount, token)
                        return {"status": True, "message":"voucher has been cashed successfully", "data": data.get("amount") }, 200
                    elif data["status"] == "cashed":
                        return {"status": False, "message":"token has been used.", "data": None}, 400
                else:
                    return {"status": False, "message":"token does not exist.", "data": None}, 400
            else:
                return {"status": False, "message":"invalid token.", "data": None}, 400
        else:
            return {"status": False, "message":"invalid phone number", "data": None}, 400       
api.add_resource(CashVoucher, "/cashvoucher/<string:userphone>")
