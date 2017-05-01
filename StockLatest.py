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
    return "None"
            
#accept input
while True:
    try:
        print("Input : ")
        symbolT = input("Please enter a symbol : ")
        company = get_symbol(symbolT.upper())
        while company.lower() in ("none","networkerror"):
            if company == "NetworkError":
                exit()
            symbolT = input("Invalid Symbol. Please enter a valid symbol : ")
            company = get_symbol(symbolT.upper())
        #display output
        print("\nOutput : ")
        dt = datetime.datetime.now(tzlocal.get_localzone())
        print(dt.strftime("%a %b %d %H:%M:%S %Z %Y"))
        print(company+" ("+symbolT.upper()+") ")
        stock = Share(symbolT)
        print(stock.get_price()+ " "+stock.get_change() + " (" +stock.get_percent_change()+") ")
        print("---------------------------------------------")
        cont = input("Do you want to continue? (Y/N) : ")
        if cont == 'Y' or cont == "y":
            continue
        else:
            break
    except ValueError:
        print("\nWrong Input! Please try again.")

