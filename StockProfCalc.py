# take input from the user
print("Stock Profit Calculator")
print("Please provide following information - ")
symbol = input("Stock Ticker symbol : ")
while True:
    try:
        allotment = float(input("Allotment (number of shares) : "))
        finalPrice = float(input("Final share price (in dollars) : "))
        sellCom = float(input("Sell commission (in dollars) : "))
        initialPrice = float(input("Inital share price (in dollars) : "))
        buyCom = float(input("Buy commission (in dollars) : "))
        tax = float(input("Captial gain tax rate (in %) : "))
        break  #break from true when all inputs are valid
    except ValueError:
        print("\nWe accept only numbers please try again.")

#profit calculations
proceeds = allotment * finalPrice
totalPurchasePrice = allotment * initialPrice
gain = proceeds - totalPurchasePrice - sellCom - buyCom
totalTax = gain*tax/100
cost = totalPurchasePrice + sellCom + buyCom + totalTax
netProfit = proceeds - cost
returnIn = 100*netProfit/cost
brkEvn = (totalPurchasePrice + buyCom +sellCom)/allotment

#display output
print("\n-----------------------------")
print("Profit Report \n")
print("\nProceeds = $","{0:,.2f}".format(proceeds))
print("\nCost = $","{0:,.2f}".format(cost))
print("\nCost Details : ")
print ("Total purchase price = $","{0:,.2f}".format(totalPurchasePrice))
print ("Tax on Capital Gain = $","{0:,.2f}".format(totalTax))
print("\nNet Profit = $","{0:,.2f}".format(netProfit))
print("\nReturn on Investment (in %) = ","{0:,.2f}".format(returnIn),"%")
print("\nTo break even, you should have a final share price of $","{0:,.2f}".format(brkEvn))
print("\n-----------------------------\n")
