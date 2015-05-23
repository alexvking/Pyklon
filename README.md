Pyklon: Full-Featured Klondike Solitaire in Python
--------------------------------------------------
By Alex King

SUMMARY
-------
Pyklon is a full-featured Klondike Solitaire engine written in Python. It is 
completely playable (and kind of fun!) in the terminal, but was designed as a 
backend that could easily power a frontend UI.

Pyklon features partial endgame detection. It does not currently detect games
where cards can be moved, but no true progress can be made.

USAGE
-----

Run <code>python main.py</code> at the terminal to play.

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
