#
# splitcosts.py: a simple cost splitter
#
# This program allows you to compute the balances of all the expenses occuring
# during a trip with friends (let's say) and to obtain a list of transfers that
# need to be done to settle this balance. Each participant can but does not need
# to participate to each of the activities. See example files in this directory.
#
# Usage:
#
#   python splitcosts.py file
#

import sys, csv, re
from decimal import Decimal
import decimal

DISPLAY_LENGTH = 23  # my favorite number


def trim(string, length):
    """Trim string to be of a certain length. For displaying.

    Inputs:
        string -- The string to trim.
        length -- The maximal allowed length. Must be bigger than 3.

    Output:       Trimed string.
    """
    assert length > 3
    return string[:length-3] + '...' if len(string)>length else string


def settle(balance):
    """Solve for the transaction to be done given a list of balances. When the
    balance is postitive (negative) it means that the corresponding person will
    receive (give) the corresponding amount. Each person does a single
    transaction and the total amount of money that is transfered is minimised.

    Inputs:
        bal -- the balance of all the participants as a dictionary with
               structure { 'name': balance } where balance is a real number.

    Output:    list of transactions as dictionaries of the form { 'in' : in,
               'out' : out, 'amount' : amount } where in and out are ids given
               in the input and amount is always positive.
    """
    # check that sum vanishes
    tot = sum(balance.values())
    if(tot!=Decimal(0)):
        #raise ValueError("total balance is non-vanishing! (tot={})".format(tot))
        print "\nNote that there is a total imbalance of {}.".format(tot)
    # erase 0 balances and transform to list
    balance = [ { 'name' : i, 'balance': balance[i] } for i in balance
                                                      if balance[i]!=0 ]
    # list of payements
    payements = []
    while(len(balance)>1):
        # sort by increasing balance
        balance.sort(key = lambda x: x['balance'])
        # add payement
        payements.append({ 'out' : balance[-1]['name'],
                           'in'  : balance[ 0]['name'],
                           'amount' : balance[-1]['balance'] })
        balance[0]['balance'] += balance[-1]['balance']
        balance.pop(-1)

    return payements


def get_balance(filename):
    """Get balances from file.

    Inputs:
        file -- the file to be read

    Output:     the list of balances
    """
    # open and read file
    with open(filename) as csvfile:

        reader = csv.reader(csvfile, skipinitialspace=True)

        # get header and participants names
        header = next(reader)
        names = [ i for i in header if i!='' ]
        balance = { name: Decimal(0) for name in names }

        # print
        print ''.join([('{:' + str(DISPLAY_LENGTH) + '}').format(h) for h in header])
        print '-'*DISPLAY_LENGTH*(len(header) - 1)

        # compute balance row by row
        exp = -2
        for row in reader:

            rownames = []
            total = Decimal(0)
            # compute running total, find out who participated, update balance
            for i in range(len(row)):
                if header[i]=='': continue
                if row[i].strip()=='-': continue
                m = re.match(r"\((.+?)\)", row[i].strip())
                if m!=None:
                    d = Decimal(m.group(1))
                else:
                    rownames += [ header[i] ]
                    d = Decimal(row[i] if row[i].strip()!='' else '0')
                amount = d
                total += amount
                balance[header[i]] -= amount
                # find working decimal precision
                exp = min(exp, d.as_tuple().exponent)

            # correct the balance by adding the share of everybody
            for n in rownames:
                balance[n] += total/Decimal(len(rownames))

            print(''.join([('{:' + str(DISPLAY_LENGTH) + '}').format(trim(str(h), DISPLAY_LENGTH-1)) for h in row]))

        # round to the nearest value (using exponent exp)
        for name in balance.keys():
            balance[name] = balance[name].quantize(Decimal('10')**exp)

        print '-'*DISPLAY_LENGTH*(len(header) - 1)
        print ''.join([('{:' + str(DISPLAY_LENGTH) + '}').format(str(balance.get(h, ''))) for h in header])

    return balance

################################################################################

if len(sys.argv)==1:
    print("Please provide an input file.")
    exit(1)

# get balance
balance = get_balance(sys.argv[1])
# and settle
p = settle(balance)

print('\nTransfers:')
for m in p:
    print " ", m['out'], "->", m['in'], ":", m['amount']
