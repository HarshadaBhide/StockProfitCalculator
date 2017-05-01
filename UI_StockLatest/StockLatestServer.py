# coding=utf-8

from flask import Flask, render_template
from flask import jsonify, request, session # import objects from the flask module
import json
from flask import Response
import requests
import datetime
import tzlocal
from yahoo_finance import Share

def get_symbol(symbol):
    url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(symbol)

    try:
        result = requests.get(url).json()
    except:
        print("\nNetwork Error. Please try after some time.")
        return "NetworkError"
    for x in result['ResultSet']['Result']:
        if x['symbol'] == symbol:
            return x['name']
    return "InvalidSymbol"

app = Flask(__name__) #define app using Flask

@app.route('/')
def index():
   return render_template('index.html')

finalResult = {}
@app.route('/result',methods = ['POST'])
def getPrice():
    input= json.dumps(request.json)
    data = input
    print(data)
    symbolT = request.json['symbol']
    finalResult["errMsg"] = "None"
    try:
        company = get_symbol(symbolT.upper())
        if company == "NetworkError" or company == "InvalidSymbol":
            finalResult["errMsg"] = company
        else:
            #output
            dt = datetime.datetime.now(tzlocal.get_localzone())
            finalResult["time"] = dt.strftime("%a %b %d %H:%M:%S %Z %Y")
            finalResult["company"] = company+" ("+symbolT.upper()+") "
            stock = Share(symbolT)
            finalResult["stockInfo"] = stock.get_price()+ " "+stock.get_change() + " (" +stock.get_percent_change()+") "
        
    except ValueError:
        finalResult["errMsg"] = "SystemError"
    
    jsonResult = json.dumps(finalResult)
    return jsonResult

if __name__ == "__main__" :
    app.run( host='0.0.0.0',port = 5000, debug = True) # run app in debug mode