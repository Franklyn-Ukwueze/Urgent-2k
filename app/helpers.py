from app import wallets, voucherdb
#import os
#from pymongo import MongoClient
import random

# client = MongoClient(os.getenv("MONGO_URI"))
# db = client.urgent2k
# wallets = db.wallets
# voucherdb = db.vouchers


def get_balance(userphone):
    if userphone.isdigit() and len(userphone) == 11:
        data = wallets.find_one({"userphone": userphone})
        if data:
            return data["balance"]
        else:
            return None
    else:
        return None

def credit(userphone, amount):
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

def debit(userphone, amount):
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

def create_voucher(userphone, amount):
    if userphone.isdigit() and len(userphone) == 11:
        if amount.isdigit():
            amount = float(amount)
            if amount > 0:
                token = str(random.randint(100000000000, 999999999999))
                while voucherdb.find_one({"token": token}):
                    token = random.randint(100000000000, 999999999999)
                voucherdb.insert_one({"token": token, "creator": userphone, "amount": amount, "status": "available", "casherphone": "null"})
                print({"token": token, "creator": userphone, "amount": amount, "status": "available", "casherphone": "null"})
            else:
                print("invalid amount.")
        else:
            print("invalid amount.")
    else:
        print("invalid userphone.")



def cash_voucher(userphone, token):
    if userphone.isdigit() and len(userphone) == 11:
        if token.isdigit() and len(token) == 12:
            data = voucherdb.find_one({"token": token})
            if data:
                if data["status"] == "available":
                    voucherdb.update_one({"token": token}, {"$set": {"status": "cashed"}})
                    voucherdb.update_one({"token": token}, {"$set": {"casherphone": userphone}})
                    print(voucherdb.find_one({"token": token}))
                elif data["status"] == "cashed":
                    print("token has been used")
            else:
                print("token does not exist.")
        else:
                print("invalid token.")
    else:
        print("invalid userphone.")        



#print(voucherdb.find_one({"token": "908891780559"})["status"])
#create_voucher("09015889838", "50")
#cash_voucher("07018168824", "908891780559")
#wallets.insert_one({"userphone": "07018168824", "balance": 100.00})
#credit("07018168824", "5000")
#debit("0701868824", "3000")
#print(get_balance("07018l68824"))       
