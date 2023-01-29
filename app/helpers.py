import os
import random
import requests
#from app import wallets, voucherdb
from pymongo import MongoClient


client = MongoClient(os.getenv("MONGO_URI"))
db = client.urgent2k
wallets = db.wallets
voucherdb = db.vouchers

urgent2k_token = os.getenv("URGENT_2K_KEY")
base_url = os.getenv("SAFEPAY_URL")

def get_balance(userphone):
    # if userphone.isdigit() and len(userphone) == 11:
    #     data = wallets.find_one({"userphone": userphone})
    #     if data:
    #         return data["balance"]
    #     else:
    #         return None
    # else:
    #     return None
    headers = {'content-type': 'application/json', 'x-access-token': f"{urgent2k_token}"}
    url = f"https://safe-payy.herokuapp.com/api/v1/urgent2k/usertransaction/balance/{userphone}"

    try:
        #Make API call
        r = requests.get(url=url, headers=headers)
        print(f"Status code: {r.status_code}")  #Print status code
        response = r.json()
    except Exception as e:
        return f"Encountered error: {e}"

    if not response.get("status"):
        return response.get("message")

    data = response.get("data") 
    return data.get("available_balance")


def credit(userphone, amount, token):
    if userphone.isdigit() and len(userphone) == 11:
        if amount.isdigit(): 
            # amount = round(float(amount), 2)
            # if amount > 0:
            #     amount = round(float(amount), 2)
            #     if get_balance(userphone):
            #         old_balance = get_balance(userphone)
            #         new_balance = old_balance + amount
            #         wallets.update_one({"userphone": userphone}, {"$set": {"balance": new_balance}})
            #     else:
            #         return None
            # else:
            #     return None
            headers = {'content-type': 'application/json', 'x-access-token': f"{urgent2k_token}"}
            data = {'amount': amount, 'desc': f'Credit!Claim of NGN{amount} gift voucher.VOUCHER:{token}'}
            url = f"https://safe-payy.herokuapp.com/api/v1/urgent2k/usertransaction/credit/{userphone}"

            try:
                #Make API call
                r = requests.post(url=url, data=data, headers=headers)
                print(f"Status code: {r.status_code}")  #Print status code
                response = r.json()
            except Exception as e:
                return f"Encountered error: {e}"

            if not response.get("status"):
                return response.get("message")

            return response
        else:
            return None
    else:
        return None

def debit(userphone, amount, token):
    if userphone.isdigit() and len(userphone) == 11:
        if amount.isdigit:
            amount = round(float(amount), 2) 
            if amount > 0:
                # if get_balance(userphone):
                #     old_balance = get_balance(userphone)
                #     if old_balance - amount > 100.00:
                #         new_balance = old_balance - amount
                #         wallets.update_one({"userphone": userphone}, {"$set": {"balance": new_balance}})
                #     else:
                #         return None
                # else:
                #     return None
                headers = {'content-type': 'application/json', 'x-access-token': f"{urgent2k_token}"}
                data = {'amount': amount, 'desc': f'Debit!Generation of NGN{amount} gift voucher.VOUCHER:{token}'}
                url = f"https://safe-payy.herokuapp.com/api/v1/urgent2k/usertransaction/debit/{userphone}"

                try:
                    #Make API call
                    r = requests.post(url=url, data=data, headers=headers)
                    print(f"Status code: {r.status_code}")  #Print status code
                    response = r.json()
                except Exception as e:
                    return f"Encountered error: {e}"

                if not response.get("status"):
                    return response.get("message")

                return response

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


#print(get_balance("08034335775"))
#print(voucherdb.find_one({"token": "908891780559"})["status"])
#create_voucher("09015889838", "50")
#cash_voucher("07018168824", "908891780559")
#wallets.insert_one({"userphone": "07018168824", "balance": 100.00})
print(credit("07018168824", "50","908891780559" ))
#debit("0701868824", "3000")
#print(get_balance("07018l68824"))       