from flask import Flask

app = Flask(__name__)
#from app import views

from app.mod_arbcalc.arbcalc import get_spread as get_spread

from flask import render_template
from app import app
import itertools

@app.route('/')
@app.route('/index')

def index():

    list_of_exchanges = ['korbit', 'kraken']

    # product('ABCD', repeat=2)
    # result =  AA AB AC AD BA BB BC BD CA CB CC CD DA DB DC DD
    # this is what I need to generate the table that I want
    combos = itertools.product(list_of_exchanges, repeat=2)
    combos_list = list(combos)

    crypto_list = ['btc', 'eth', 'xrp', 'etc']

    all_spreads = []

    for curr in crypto_list:
        table_data2 = []
        print("-----\ncurrency: %s" % curr)
        for pair in combos_list:
            print("----\npair:")
            print(pair)
            a = {'name': pair[0]}
            b = {'name': pair[1]}
            this_spread = get_spread(a, b, curr)
            print(this_spread)
            table_data2.append(this_spread)

        # a = {'name': 'korbit'}
        # b = {'name': 'kraken'}

        print(table_data2)
        # for item in table_data2:
        #     print("here: %s" % item)

        # example table data
        table_data = [
            ["", "korbit", "kraken"],
            ["korbit", "0", "30%"],
            ["kraken", "-30%", "0"]
        ]

    user = {'nickname': ' '}  # fake user
    return render_template('index.html',
                           user=user,
                           table_data=table_data,
                           all_spreads=all_spreads)
