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

    list_of_exchanges = ['korbit', 'kraken', 'quadriga', 'bitso']


    combos = itertools.combinations(list_of_exchanges, 2)
    combos_list = list(combos)

    # # product('ABCD', repeat=2)
    # # result =  AA AB AC AD BA BB BC BD CA CB CC CD DA DB DC DD
    # # this is what I need to generate the table that I want
    # combos = itertools.product(list_of_exchanges, repeat=2)
    # combos_list = list(combos)

    #crypto_list = ['btc', 'eth', 'xrp', 'etc']
    crypto_list = ['btc', 'eth']

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
            try:
                title = a + " / " + b
                table_data2.append([title, a, b])
            except:
                print("Couldn't get spread.")
        

        all_pairs.append((curr, table_data2))

    user = {'nickname': ' '}  # fake user
    return render_template('index.html',
                           user=user,
                           table_data=table_data2,
                           all_pairs=all_pairs,
                           list_of_exchanges=jsonify(list_of_exchanges))


@app.route('/get_curr_price_from_exchange')
def get_curr_price_from_exchange():
    currency = request.args.get('currency', "", type=str)
    exchange = request.args.get('exchange', "", type=str)

    price = get_price(currency, exchange)
    return jsonify(price)
