# splitcosts
Settle bills from csv file.

This program allows you to compute the balances of all the expenses occuring
during a trip with friends (let's say) and to obtain a list of transfers that
need to be done to settle this balance. Each participant can but does not need
to participate to each of the activities.

Usage: `python splitcosts.py file`

The first line is the header line and gives the name of participants. Any column
whose header line is empty is discarded. This is useful to include comments.
Each subsequent line defines the contributions of each person to a single event.
Each entry can be:
* a number, to indicate that the person did participate the event and paid the
  given amount.
* empty or `0` to indicate that the person did participate the event but did not
  pay anything.
* `-` to indicate that the person did not participate the event and does not
  need to pay for it.
* a number in parentheses, to indicate that the person paid for others, i.e.
  paid but did not participate.
See example file in this directory.

Once the total balance is obtained a simple algorithm computes a list of
transfers that can be made to settle this balance. A maximium of a single 
transfer is always necessary to settle the bill!
