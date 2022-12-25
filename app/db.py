from pymongo import MongoClient
import os

client = MongoClient(os.getenv("MONGO_URI"))
db = client.urgent2k

wallets = db.wallets

def get_balance(userphone):
    if userphone.is_digit() and len(userphone) == 11:
        data = wallets.find_one({"userphone": userphone})
        if data:
            return data["balance"]
        else:
            return None
    else:
        return None

def credit(userphone, amount):
    if userphone.is_digit() and len(userphone) == 11:
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

def debit(userphone, amount):
    if userphone.is_digit() and len(userphone) == 11:
        if amount > 0:
            amount = round(float(amount), 2)
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


            
