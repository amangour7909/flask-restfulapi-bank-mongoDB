from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)

@app.route('/')
def home():
    return "Welcome to the Bank Flask API!"

client = MongoClient("mongodb://localhost:27017")
db = client.BankAPI
users = db["Users"]

def userExist(username):
    count = users.count_documents({"Username": username})
    return count > 0
    
def generateResponse(status, message):
    return jsonify({
        "status": status,
        "message": message
    })

class Register(Resource):
    def post(self):
        postedData = request.get_json()

        if not "username" in postedData or not "password" in postedData:
            return generateResponse(301, "Missing Information")
        
        username = postedData["username"]
        password = postedData["password"]

        if userExist(username):
            return generateResponse(301, "User already exists")

        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        users.insert_one({
            "Username": username,
            "Password": hashed_pw,
            "Balance": 0,
            "Debt": 0
        })

        return generateResponse(200, "You successfully registered")

def verifyPw(username, password):
    if not userExist(username):
        return False

    hashed_pw = users.find({"Username":username})[0]["Password"]

    if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
        return True
    else:
        return False
    
# def cashWithUser(username):
#     cash = users.find_one({"Username":username})[0]["Balance"]
#     return cash

def cashWithUser(username):
    user = users.find_one({"Username": username})
    if user:
        return user["Balance"]
    return 0  # or raise an exception based on your needs

def debtWithUser(username):
    user = users.find_one({"Username": username})
    if user:
        return user["Debt"]
    return 0  # or raise an exception based on your needs

def updateBalance(username, balance):
    users.update_one({"Username":username}, {"$set":{"Balance":balance}})

def updateDebt(username, debt):
    users.update_one({"Username":username}, {"$set":{"Debt":debt}})

class Add(Resource):
    def post(self):
        postedData = request.get_json()

        if not "username" in postedData or not "password" in postedData or not "amount" in postedData:
            return generateResponse(301, "Missing Information")

        username = postedData["username"]
        password = postedData["password"]
        amount = postedData["amount"]

        if not userExist(username):
            return generateResponse(301, "Invalid Username")

        correct_pw = verifyPw(username, password)
        if not correct_pw:
            return generateResponse(302, "Invalid Password")

        if amount <= 0:
            return generateResponse(304, "Amount must be greater than 0")
        
        if username == "BANK":
            bankBalance = cashWithUser("BANK")
            users.update_one({"Username": "BANK"}, {"$set": {"Balance": bankBalance + amount}})
            return generateResponse(200, "Amount added successfully")

        bankBalance = cashWithUser("BANK")
        bankBalance += 1
        userBalance = cashWithUser(username)
        amount -= 1
        amount = amount + userBalance

        if bankBalance - amount < 0:
            return generateResponse(305, "Not enough money in the bank")
        updateBalance(username, amount)
        updateBalance("BANK", bankBalance - amount)

        return generateResponse(200, "Amount added successfully")
    
class Transfer(Resource):
    def post(self):
        postedData = request.get_json()

        if not "username" in postedData or not "password" in postedData or not "to" in postedData or not "amount" in postedData:
            return generateResponse(301, "Missing Information")

        username = postedData["username"]
        password = postedData["password"]
        to = postedData["to"]
        amount = postedData["amount"]

        if not userExist(username) or not userExist(to):
            return generateResponse(301, "Invalid Username - sender")
        
        if username == to:
            return generateResponse(306, "Cannot transfer to the same account")   
        
        if not userExist(to):
            return generateResponse(301, "Invalid Username - recipient")

        correct_pw = verifyPw(username, password)
        if not correct_pw:
            return generateResponse(302, "Invalid Password")

        if amount <= 0:
            return generateResponse(304, "Amount must be greater than 0")
        
        if cashWithUser(username) < amount:
            return generateResponse(305, "Not enough money in the account")
        
        userBalance = cashWithUser(username)
        toBalance = cashWithUser(to)
        updateBalance(username, userBalance - amount)
        updateBalance(to, toBalance + amount)

        return generateResponse(200, "Amount transferred successfully")
    
class CheckBalance(Resource):
    def post(self):
        postedData = request.get_json()

        if not "username" in postedData or not "password" in postedData:
            return generateResponse(301, "Missing Information")

        username = postedData["username"]
        password = postedData["password"]

        if not userExist(username):
            return generateResponse(301, "Invalid Username")

        correct_pw = verifyPw(username, password)
        if not correct_pw:
            return generateResponse(302, "Invalid Password")

        balance = cashWithUser(username)
        debt = debtWithUser(username)

        return generateResponse(200, "Balance: " + str(balance) + " Debt: " + str(debt))
    
class TakeLoan(Resource):
    def post(self):
        postedData = request.get_json()

        if not "username" in postedData or not "password" in postedData or not "amount" in postedData:
            return generateResponse(301, "Missing Information")

        username = postedData["username"]
        password = postedData["password"]
        amount = postedData["amount"]

        if not userExist(username):
            return generateResponse(301, "Invalid Username")

        correct_pw = verifyPw(username, password)
        if not correct_pw:
            return generateResponse(302, "Invalid Password")

        if amount <= 0:
            return generateResponse(304, "Amount must be greater than 0")

        bankBalance = cashWithUser("BANK")
        userBalance = cashWithUser(username)
        userDebt = debtWithUser(username)

        if bankBalance < amount:
            return generateResponse(305, "Not enough money in the bank")

        updateBalance("BANK", bankBalance - amount)
        updateBalance(username, userBalance + amount)
        updateDebt(username, userDebt + amount)

        return generateResponse(200, "Loan taken successfully")
    
class PayLoan(Resource):
    def post(self):
        postedData = request.get_json()

        if not "username" in postedData or not "password" in postedData or not "amount" in postedData:
            return generateResponse(301, "Missing Information")

        username = postedData["username"]
        password = postedData["password"]
        amount = postedData["amount"]

        if not userExist(username):
            return generateResponse(301, "Invalid Username")

        correct_pw = verifyPw(username, password)
        if not correct_pw:
            return generateResponse(302, "Invalid Password")

        if amount <= 0:
            return generateResponse(304, "Amount must be greater than 0")

        bankBalance = cashWithUser("BANK")
        userBalance = cashWithUser(username)
        userDebt = debtWithUser(username)

        if userBalance < amount:
            return generateResponse(305, "Not enough money in the account")

        updateBalance("BANK", bankBalance + amount)
        updateBalance(username, userBalance - amount)
        updateDebt(username, userDebt - amount)

        return generateResponse(200, "Loan paid successfully")
    
api.add_resource(Register, '/register')
api.add_resource(Add, '/add')   
api.add_resource(Transfer, '/transfer')
api.add_resource(CheckBalance, '/balance')
api.add_resource(TakeLoan, '/takeLoan')
api.add_resource(PayLoan, '/payLoan')

if __name__ == '__main__':
    app.run(debug=True)