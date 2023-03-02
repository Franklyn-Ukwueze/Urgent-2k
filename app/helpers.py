import os
import random
import requests
#from app import wallets, voucherdb
from pymongo import MongoClient
from functools import wraps
from flask import request


client = MongoClient(os.getenv("MONGO_URI"))
db = client.urgent2k
wallets = db.wallets
voucherdb = db.vouchers

urgent2k_token = os.environ.get("URGENT_2K_KEY")
base_url = os.getenv("SAFEPAY_URL")

# decorator function frequesting api key as header
def urgent2k_token_required(f):
    @wraps(f)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        
        if not token:
            return {"status": False, "message": "Access token is missing at " + request.url, "data": None}, 401

        if token == urgent2k_token:
            return f(*args, **kwargs)
        else:
            return {"status": False, "message": "Invalid access token at " + request.url, "data": None}, 401

    return decorated

def get_txn(userphone):
    if userphone.isdigit() and len(userphone) == 11:
        headers = {'content-type':'application/json', 'x-access-token':f'{urgent2k_token}'}
        url = f"https://safe-payy.herokuapp.com/api/v1/urgent2k/usertransaction/retrieve/{userphone}"

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
        return data
    else:
        return "invalid phone number."

def get_balance(userphone):
    if userphone.isdigit() and len(userphone) == 11:
    #     data = wallets.find_one({"userphone": userphone})
    #     if data:
    #         return data["balance"]
    #     else:
    #         return None
    # else:
    #     return None
        headers = {'content-type':'application/json', 'x-access-token':f'{urgent2k_token}'}
        url = f"{base_url}/api/v1/urgent2k/usertransaction/balance/{userphone}"

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
    else:
        return "invalid phone number."


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
            headers = {'content-type': 'application/json', 'x-access-token':f'{urgent2k_token}'}
            payload = {'amount': amount, 'desc': f'Credit!Claim of NGN{amount} gift voucher.VOUCHER:{token}'}
            url = f"{base_url}/api/v1/urgent2k/usertransaction/credit/{userphone}"

            try:
                #Make API call
                r = requests.post(url=url, json=payload, headers=headers)
                print(f"Status code: {r.status_code}")  #Print status code
                response = r.json()
            except Exception as e:
                return f"Encountered error: {e}"

            if not response.get("status"):
                return response.get("message")

            return response
        else:
            return "amount isn't a digit"
    else:
        return "invalid phone number."

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
                headers = {'content-type': 'application/json', 'x-access-token': f'{urgent2k_token}'}
                payload = {'amount': amount, 'desc': f'Debit!Generation of NGN{amount} gift voucher.VOUCHER:{token}'}
                url = f"{base_url}/api/v1/urgent2k/usertransaction/debit/{userphone}"

                try:
                    #Make API call
                    r = requests.post(url=url, json=payload, headers=headers)
                    print(f"Status code: {r.status_code}")  #Print status code
                    response = r.json()
                except Exception as e:
                    return f"Encountered error: {e}"

                if not response.get("status"):
                    return response.get("message")

                return response

            else:
                return "invalid amount"
        else:
            return "amount isn't a digit"
    else:
        return "invalid userphone"

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

def create(userphone, amount):
    headers = {'content-type': 'application/json', 'x-access-token':'2K!@IDL_8@W!7198hU8G6l7Q18c0vXc!Ap'}
    payload = {'amount': amount}
    url = f"https://urgent-twok.onrender.com/createvoucher/{userphone}"

    try:
        #Make API call
        r = requests.post(url=url, json=payload, headers=headers)
        print(f"Status code: {r.status_code}")  #Print status code
        response = r.json()
    except Exception as e:
        return f"Encountered error: {e}"

    # if not response.get("status"):
    #     return response.get("message")

    return response

def get_inflow(userphone):
    if userphone.isdigit() and len(userphone) == 11:
        headers = {'content-type':'application/json', 'x-access-token':f'{urgent2k_token}'}
        url = f"{base_url}/api/v1/urgent2k/usertransaction/retrieve/{userphone}"

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
        
        total = 0
        for txn in data.get("transactions"):
            if txn.get("alert") == "Credit":
                total = total + float(txn.get("amount")[3:])
            else:
                continue
        return total
    else:
        return "invalid phone number."
    
def get_outflow(userphone):
    if userphone.isdigit() and len(userphone) == 11:
        headers = {'content-type':'application/json', 'x-access-token':f'{urgent2k_token}'}
        url = f"{base_url}/api/v1/urgent2k/usertransaction/retrieve/{userphone}"

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
        
        total = 0
        for txn in data.get("transactions"):
            if txn.get("alert") == "Debit":
                total = total + float(txn.get("amount")[3:])
            else:
                continue
        return total
    else:
        return "invalid phone number."
    
def get_txn_history(userphone, count=None):
    if userphone.isdigit() and len(userphone) == 11:
        headers = {'content-type':'application/json', 'x-access-token':f'{urgent2k_token}'}
        url = f"{base_url}/api/v1/urgent2k/usertransaction/retrieve/{userphone}"

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
        transactions = data.get("transactions")

        if count:
            if count.isdigit():
                int(count)
                return transactions[:-abs(count):-1]
            else:
                return "count has to be a number"
        else:
            return transactions[::-1]

    else:
        return "invalid phone number."
    




#print(create("09015889838", "50"))
#print(get_txn("08034335775"))
#print(voucherdb.find_one({"token": "908891780559"})["status"])
#create_voucher("09015889838", "50")
#cash_voucher("07018168824", "908891780559")
#wallets.insert_one({"userphone": "07018168824", "balance": 100.00})
#print(credit("08034335775", "50","908891780559" ))
#print(debit("08034335775", "50","908891780559"))
#print(get_outflow("08034335775")) 
#print(get_inflow("08034335775")) 
#print(get_txn_history("08034335775", 5))     