Pyklon: Full-Featured Command Line Klondike Solitaire
-----------------------------------------------------
By Alex King

<img src="screen.png">

Summary
-------
Pyklon is full-featured Klondike solitaire written in Python. It is 
completely playable (and kind of fun!) in the terminal, but it was more created
as an engine that could eventually power a UI.

Pyklon has features on par with the best digital solitaire games available today. 
It features <b>undo</b>, a <b>hint engine</b>, robust <b>endgame detection</b>,
<b>automatic solving for winnable games</b>, and even an experimental <b>autoplay</b>
feature.

Usage and Tips
--------------

Run <code>python main.py</code> at the terminal to play.

Pyklon works by taking in addresses for the source and destination for any 
given move. The seven columns (tableaus) are addressed with numbers 1-7, followed
by a row 1-19. 

The four accumulation stacks (foundations) are addressed as A1, A2, A3 and A4.

The top card of the draw pile is addressed as DC.

Some example moves are "11 22", "DC 54", "32 A3", and "719 111".

Endgame detection in the game requires use of the hint system, which will suggest
possible moves as long as they are unique. This detection is more powerful than
some other digital versions of solitaire, which sometimes only detect playability
based on cards available in the draw pile.

Here's how the endgame detection improves upon that:
Because movement between two tableaus should always either uncover a card or expose
another, lateral movements between two tableaus are kept track of so that each
unique lateral move will only ever be suggested once. In this way, if the game has no more
useful moves that can uncover cards and advance the game, the hint system may 
suggest that the player move a card stack from
position A to position B, but it will not recommend the reverse, and it will not
make the same recommendation again.

If you want to make sure the game detects if you have no more possible
moves, make sure to request a few hints and do the moves that it suggests.

To play around with the autoplay feature, you can either type "autoplay" while
playing, or run <code>python auto.py</code> to run a simulation of nonstop
autoplay. Use <code>CTRL + C</code> to end the simulation and see how many games
were won and how many were lost.

Known Issues and Planned Improvements
-------------------------------------

Pyklon highlights cards with UNIX-compatible unicode characters. If you're on 
Windows, the game won't display properly. Just use a Unix terminal emulator like 
<a href="http://gooseberrycreative.com/cmder/">cmder</a>.

Unlimited undo would be a relatively easy feature to add, but I have not
implemented it because I don't believe it's the way the game was meant to be played.

Right now, the hint engine will suggest any valid move (according to the algorithm
described above). It does not catch itself before recommending a move that will
lead to an unplayable board. For example, the hint engine will require a player
to move a stack of 5432 from one 6 to another, even if it doesn't create a new
movement opportunity by exposing a 6. This is a small thing, but if this feature were
added, hints would be more realistic, and endgame detection would work more quickly.

Right now, Pyklon does not store any statistics about played games. A future 
update could track wins, losses, and the best time to finish.

Scoring may also be added in a future version.

Version History and Release Notes
---------------------------------

5/25/15 VERSION 1.3.1
  - Fixed bug where bad foundation coordinates could crash the program
  - Fixed bug where improper input still caused previous game state to be overwritten

5/25/15 VERSION 1.3
- Added solve functionality

5/23/15 VERSION 1.2
  - Added undo support

5/23/15 VERSION 1.1
  - Complete endgame detection added

5/22/15 VERSION 1.0
  - Initial release
