# coding=utf-8

from flask import Flask, render_template
from flask import jsonify, request, session # import objects from the flask module
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
from sqlalchemy import event
from sqlalchemy import DDL
import requests
from flask import Response

app = Flask(__name__) #define app using Flask

@app.route('/v1/locations/', methods=['POST'])
def post_location():
    input_json = request.get_json(force=True)
    name = request.json['name']
    address = request.json['address']
    city = request.json['city']
    state = request.json['state']
    zip = request.json['zip']
    createdOn = datetime.now()
    updatedOn = datetime.now()

    print(name)
    print(address)
    print(city)
    print(state)
    print(zip)

    url = ("http://maps.google.com/maps/api/geocode/json?address="+name+",+"+address+",+"+city+",+"+state+",+"+zip+"&sensor=false")
    req_url = url.replace(" ","+")
    response = urllib2.urlopen(req_url)
    json_response = response.read()
    jsonList = json.loads(json_response)
    lat = jsonList["results"][0]["geometry"]["location"]["lat"]
    lng = jsonList["results"][0]["geometry"]["location"]["lng"]
    print(lat)
    print(lng)

    record = LocationDetails(name,address,city,state,zip,createdOn, updatedOn, lat, lng)
    #db.create_all();
    db.session.add(record)
    db.session.commit()
    record = LocationDetails.query.filter_by(name=name).first_or_404()
    return jsonify(result=[record.serialize]), 201

@app.route('/')
def index():
   return render_template('index.html')

finalResult = {}
@app.route('/result',methods = ['POST'])
def getPrice():
    input= json.dumps(request.json)
    data = input
    print(data)
    allotment = float(request.json['allotment'])
    finalPrice = float(request.json['finalPrice'])
    sellCom = float(request.json['sellCom'])
    buyCom = float(request.json['buyCom'])
    initialPrice = float(request.json['initialPrice'])
    tax = float(request.json['gainPerc'])
    
    proceeds = allotment * finalPrice
    finalResult["proceeds"] = "{0:,.2f}".format(proceeds)
    finalResult["totalPurchasePrice"] = allotment * initialPrice
    finalResult["gain"] = proceeds - finalResult["totalPurchasePrice"] - sellCom - buyCom
    finalResult["totalTax"] = finalResult["gain"]*tax/100
    cost = finalResult["totalPurchasePrice"] + sellCom + buyCom + finalResult["totalTax"]
    finalResult["cost"] = "{0:,.2f}".format(cost)
    netProfit = proceeds - cost
    finalResult["netProfit"] = "{0:,.2f}".format(netProfit)
    finalResult["returnIn"] = "{0:,.2f}".format( 100*netProfit/cost )
    finalResult["brkEvn"] = "{0:,.2f}".format( (finalResult["totalPurchasePrice"] + buyCom +sellCom)/allotment)

    jsonResult = json.dumps(finalResult)
    return jsonResult

if __name__ == "__main__" :
    app.run( host='0.0.0.0',port = 5000, debug = True) # run app in debug mode