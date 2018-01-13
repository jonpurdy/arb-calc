from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
#from app import views

from app.mod_arbcalc.arbcalc import get_price as get_price
from app.mod_arbcalc.arbcalc import get_spread as get_spread

from app import app
import itertools



@app.route('/')
@app.route('/index')

def index():

    global list_of_exchanges
    global list_of_currencies
    list_of_currencies = ['btc', 'eth']
    list_of_exchanges = ['korbit', 'kraken', 'quadriga', 'bitso']

    combos = itertools.combinations(list_of_exchanges, 2)
    combos_list = list(combos)

    # # product('ABCD', repeat=2)
    # # result =  AA AB AC AD BA BB BC BD CA CB CC CD DA DB DC DD
    # # this is what I need to generate the table that I want
    # combos = itertools.product(list_of_exchanges, repeat=2)
    # combos_list = list(combos)

    #crypto_list = ['btc', 'eth', 'xrp', 'etc']
    crypto_list = ['btc', 'eth', 'xrp']

    all_pairs = []

    # for each currency
    for curr in crypto_list:
        table_data2 = []
        print("-----\ncurrency: %s" % curr)

        # now, let's generate a table for one currency
        row = []
        for pair in combos_list:

            print("----\npair:")
            print(pair)
            a = pair[0]
            b = pair[1]

            title = a + " / " + b
            table_data2.append([title, a, b])
        

        all_pairs.append((curr, table_data2))

    return render_template('index.html',
                           table_data=table_data2,
                           all_pairs=all_pairs,
                           list_of_exchanges=jsonify(list_of_exchanges),
                           combos_list=combos_list)

@app.route('/get_currencies')
def get_currencies():
    return jsonify(list_of_currencies)

@app.route('/get_exchanges')
def get_exchanges():
    return jsonify(list_of_exchanges)


@app.route('/get_exchange_pairs')
def get_exchange_pairs():
    combos = itertools.combinations(list_of_exchanges, 2)
    combos_list = list(combos)

    currency_and_exchange_pairs = []
    for curr in list_of_currencies:
        for pair in combos_list:
            currency_and_exchange_pairs.append(curr + "-" + pair[0] +  "-" + pair[1])
    return jsonify(currency_and_exchange_pairs)

@app.route('/get_curr_price_from_exchange')
def get_curr_price_from_exchange():
    currency = request.args.get('currency', "", type=str)
    exchange = request.args.get('exchange', "", type=str)

    price = get_price(currency, exchange)
    return jsonify(price)

@app.route('/get_spread_now')
def get_spread_now():
    # currency = request.args.get('currency', "", type=str)
    # exchange1 = request.args.get('exchange1', "", type=str)
    # exchange2 = request.args.get('exchange2', "", type=str)
    it = request.args.get('exch_pair', "", type=str)
    currency, exchange1, exchange2 = it.split("-")
    print(exchange1, exchange2, currency)

    spread, a_price, b_price = get_spread(exchange1, exchange2, currency)
    return spread

@app.route('/get_spread_historical')
def get_spread_historical():
    currency = request.args.get('currency', "", type=str)
    exchange1 = request.args.get('exchange1', "", type=str)
    exchange2 = request.args.get('exchange2', "", type=str)
    when = request.args.get('date', "", type=str)

    spread = get_price(currency, exchange)
    return jsonify(price)

if __name__ == "__main__":
    application.run(host='0.0.0.0')
