from app import wallets

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

#wallets.insert_one({"userphone": "07018168824", "balance": 100.00})
#credit("07018168824", "5000")
#debit("0701868824", "3000")
#print(get_balance("07018l68824"))       
