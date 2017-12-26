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

    list_of_exchanges = ['korbit', 'kraken', 'quadriga', 'bitso']


    combos = itertools.combinations(list_of_exchanges, 2)
    combos_list = list(combos)

    # # product('ABCD', repeat=2)
    # # result =  AA AB AC AD BA BB BC BD CA CB CC CD DA DB DC DD
    # # this is what I need to generate the table that I want
    # combos = itertools.product(list_of_exchanges, repeat=2)
    # combos_list = list(combos)

    #crypto_list = ['btc', 'eth', 'xrp', 'etc']
    crypto_list = ['btc', 'eth', 'xrp', 'etc']

    all_spreads = []

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
                this_spread, a_price, b_price, title = get_spread(a, b, curr)
                table_data2.append([title, a_price, b_price, this_spread])
                print("%s %s" % (title, this_spread))
            except:
                print("Couldn't get spread.")
    
            
            
            # # just append the spread to the row
            # if len(row) < len(list_of_exchanges):
            #     row.append(this_spread)

            # # time for a new row; append the old row to the table
            # # then create a new one, and append the spread to the new row
            # elif len(row) == len(list_of_exchanges):
            #     print("len(row): %s, len(list_of_exchanges): %s" % (len(row), len(list_of_exchanges)))
            #     table_data2.append(row)
            #     row = []
            #     row.append(this_spread)

        # # this appends the final unappended row
        # table_data2.append(row)
        print("table_data2:\n%s" % table_data2)

        # example table data
        table_data = [
            ["", "korbit", "kraken"],
            ["korbit", "0", "30%"],
            ["kraken", "-30%", "0"]
        ]

        all_spreads.append((curr, table_data2))

    user = {'nickname': ' '}  # fake user
    return render_template('index.html',
                           user=user,
                           table_data=table_data2,
                           all_spreads=all_spreads)
