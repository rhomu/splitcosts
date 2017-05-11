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

import sys, csv

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
    if(sum(balance.values())!=0):
        raise ValueError("total balance is non-vanishing!")
    # erase 0 balances and transform to list
    balance = [ { 'name' : i, 'balance': balance[i] } for i in balance
                                                      if balance[i]!=0 ]
    # list of payements
    payements = []
    while(len(balance)>1):
        # sort by increasing balance
        balance.sort(key = lambda x: x['balance'])
        # add payement
        payements.append({ 'out' : balance[ 0]['name'],
                           'in'  : balance[-1]['name'],
                           'amount' : -balance[0]['balance'] })
        balance[-1]['balance'] += balance[0]['balance']
        balance.pop(0)

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
        balance = { name: 0 for name in names }

        # print
        print ''.join(['{:15}'.format(h) for h in header])
        print '-'*15*len(header)

        # compute balance row by row
        for row in reader:

            rownames = []
            total = 0.
            # compute running total, find out who participated, update balance
            for i in range(len(row)):
                if header[i]=='': continue
                if row[i].strip()=='-': continue
                rownames += [ header[i] ]
                amount = float(row[i])
                total += amount
                balance[header[i]] -= amount

            # correct the balance by adding the share of everybody
            for n in rownames:
                balance[n] += total/len(rownames)

            print(''.join(['{:15}'.format(h) for h in row]))

        print '-'*15*len(header)
        print ''.join(['{:15}'.format(str(balance.get(h, ''))) for h in header])

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
