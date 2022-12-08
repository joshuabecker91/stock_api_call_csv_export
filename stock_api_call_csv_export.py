import requests
import time
import json
import csv

api_key = 'ce5q632ad3i4fps3aufgce5q632ad3i4fps3aug0'
stock_list = ['AAPL','AMZN','NFLX','META','GOOG']

# --------------------------------------------------------------------------------------------------------------------------

def get_stock_price(ticker, api_key):
    url = f"https://finnhub.io/api/v1/quote?symbol={ticker}&token={api_key}"
    # print(url)
    request = requests.get(url)
    data = json.loads(request.content)
    print(data['c'])
    return data['c']

# --------------------------------------------------------------------------------------------------------------------------

def get_most_volatile_stock(stock_list, api_key):
    # could store all of this in a hashmap / dictionary easily. Code is easier to read this way so left it like this for now.
    stock_symbol = ""
    percentage_change = 0
    max = 0
    current_price = 0
    last_close_price = 0
    # if we were concerned about how many api calls we are doing, and speed efficiency we could do one call with entire stock list
    for ticker in stock_list:
        url = f"https://finnhub.io/api/v1/quote?symbol={ticker}&token={api_key}"
        request = requests.get(url)
        data = json.loads(request.content)
        actual_percentage = (data['c'] - data['pc']) / data['pc'] * 100
        print(ticker, round(actual_percentage,2), "%") # can comment this out. helpful for seeing that it is working properly
        if abs(actual_percentage) > max:
            stock_symbol = ticker
            percentage_change = actual_percentage
            max = abs(actual_percentage) # using absolute because you are asking for the largest move up or down
            current_price = data['c']
            last_close_price = data['pc']
    print(stock_symbol, round(percentage_change,2),"%", current_price, last_close_price)
    # Could have this csv file as a seperate function if you prefer
    with open('most_volatile_stock.csv', 'w', newline='') as csvfile:
        fieldnames = ['stock_symbol', 'percentage_change', 'current_price', 'last_close_price']
        thewriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        thewriter.writeheader()
        thewriter.writerow({'stock_symbol' : stock_symbol, 'percentage_change' : round(percentage_change,2), 'current_price' : current_price, 'last_close_price' : last_close_price})
    return stock_symbol

    # if we wanted to pass any of this data to front end
    # return render_template('index.html', data=data['all'])

# --------------------------------------------------------------------------------------------------------------------------

# 1. Get the latest price for: Apple, Amazon, Netflix, Facebook, Google.
get_stock_price("AAPL", api_key)
get_stock_price("AMZN", api_key)
get_stock_price("NFLX", api_key)
get_stock_price("META", api_key) # formerly fb
get_stock_price("GOOG", api_key) # or googl


# 2. Get the most volatile stock (absolute percentage) AND 
# 3. Save the following information for the most volatile stock 
# to a CSV file with the following rows. Please also include the header in the CSV file:
# stock_symbol,percentage_change,current_price,last_close_price
# AAPL, 13.2, 120.5, 150
get_most_volatile_stock(stock_list, api_key)

