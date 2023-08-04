# slidePuzzle
Slide Puzzle Game

    The overall design of this slide puzzle is a mixture of procedural programming
and object oriented design. The code is anchored around two classes, Board
and Tile. The Board class loads and manages the tiles and buttons that make up
the gameboard. This is where the puzzle gets loaded, player moves get tracked,
the button functionality gets created, and where the gameplay is. The Tile
class creates the individual tiles, and allows each tile to know it's position,
what image is in it, and whether or not the tile was clicked on.
    The procedural programming pieces involve more of the initial setup of the
board, including drawing the outlines to the different sections of the screen,
loading the leaderboard, and creating some helper functions that are called
in the Board class.
