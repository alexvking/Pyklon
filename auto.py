# This is an automatic player for Solitaire. It will keep track of wins and
# losses. Use CTRL + C to quit and see the tally.

from Solitaire import Solitaire

wins = 0
losses = 0

while True:
    try:
        sol = Solitaire()
        if sol.auto_run() == True:
            wins += 1
        else:
            losses += 1
    except KeyboardInterrupt:
        print "\nWins: " + str(wins)
        print "Losses: " + str(losses)
        exit(1)