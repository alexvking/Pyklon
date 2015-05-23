Pyklon: Full-Featured Klondike Solitaire in Python
--------------------------------------------------
By Alex King

<img src="screen.png">

SUMMARY
-------
Pyklon is a full-featured Klondike Solitaire engine written in Python. It is 
completely playable (and kind of fun!) in the terminal, but was designed as a 
backend that could easily power a frontend UI.

Pyklon features a hint engine and partial endgame detection. It does not 
currently detect games where cards can be moved, but no true progress can be made.

USAGE
-----

Run <code>python main.py</code> at the terminal to play.

Pyklon works by taking in addresses for the source and destination for any 
given move. The seven columns (tableaus) are addressed with numbers 1-7, followed
by a row 1-19. 

The four accumulation stacks (foundations) are addressed as A1, A2, A3 and A4.

The top card of the draw pile is addressed as DC.

Some example moves are "11 22", "DC 54", "32 A3", and "719 111".

KNOWN ISSUES AND PLANNED IMPROVEMENTS
-------------------------------------

As stated above, Pyklon does not currently detect "futile" games. It can only
recognize when no further moves are possible.

Right now, Pyklon does not store any statistics about played games. A future 
update could track wins, losses, and the best time to finish.


VERSION HISTORY AND RELEASE NOTES
---------------------------------

5/22/15 VERSION 1.0
  - Initial release
