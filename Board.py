
import turtle, math, time, logging
from Tile import Tile
import process_puzzle, gameboard

class Board:
    """
        Board Class loads and manages the tiles and buttons that make up
        the tile swap gameboard.
    """

    def __init__(self, tr, screen, puzzle_file, moves_allowed,
                 buttons, name, leaders):
        """
            Method __init__ initializes a new board with tiles.
            Parameters:
                tr (turtle): turtle to draw the tiles
                screen (screen): screen to draw on
                puzzle_file (str): .puz file to load
                moves_allowed (int): user inputted number of moves
                buttons (list): list of quit, load, reset buttons
                name (str): user inputted name of player
                leaders (list): list of past winners for leaderboard
        """
        self.add_buttons(buttons) # add in load, reset, quit buttons
        self.tr = tr
        self.screen = screen

        # create shuffled board
        self.tiles = self.add_puzzle(tr, screen, puzzle_file, False)
        
        # sets board position of the tiles
        self.set_tile_position(self.tiles)
        self.moves = 0
        self.moves_allowed = moves_allowed
        self.name = name
        self.leaders = leaders

        # new turtle for tracking player moves and screen messages
        self.tr2 = turtle.Turtle() # used for Tracking Player moves
        self.tr2.hideturtle()

        # error logger
        self.logger = gameboard.format_logger('5001_puzzle.err')


    ###########################
    #      Getter/Setter      #
    ###########################
    def set_tile_position(self, tiles):
        """
            Method set_tile_position sets tile row and column
            position on the board.
        """
        lngth = len(tiles)
        sqrt = math.sqrt(lngth)

        # row of tile = floor division, col = modulus division
        for i in range(lngth):
            row = i // sqrt
            col = i % sqrt
            tiles[i].set_board_pos(row, col)


    def get_moves(self):
        """
            Method get_moves returns the number of moves taken
            by the player.
        """
        return self.moves


    ###########################
    #      Click Actions      #
    ###########################
    def record_click(self, x, y):
        """
            Method record_click records the click coordinates.
            Parameters:
                x (float): x coordinate of click
                y (float): y coordinate of click
        """
        self.click_x = x
        self.click_y = y


    def check_solved(self):
        """
            Method check_solved checks if the current puzzle is winning
            by comparing it to the solved puzzle.
        """
        is_solved = True
        for i in range(len(self.tiles)):
            if not self.tiles[i].is_home():
                is_solved = False # if any tile is wrong, return False
        return is_solved

    
    def check_if_clicked(self, x, y):
        """
            Function check_if_clicked checks which tile was clicked
            and returns that tile.
            Parameters:
                x (float): x coordinate of click
                y (float): y coordinate of click
            Returns tile that was clicked on, and True 
        """
        self.record_click(x, y)
        # checks each tile to see if it was clicked
        for tile in self.tiles:
            if tile.clicked_in_region(x, y):
                return tile, True
        return None, False


    def swap_tiles(self, x, y):
        """
            Method swap_tiles swaps the clicked on tile with the
            blank tile if they'r adjacent.
            Parameters:
                x (float): x coordinate of click
                y (float): y coordinate of click
            Returns True if tiles were swapped
        """
        # determine which tile was clicked
        clicked_tile = self.check_if_clicked(x, y)[0]
        # swap tile if applicable
        for tile in self.tiles:
            # swaps if adjacent and blank
            if tile.is_adjacent(clicked_tile) and tile.is_blank():
                clicked_tile.swap(tile)
                # increment moves += 1
                self.track_player_moves(self.tr2, self.screen)
                return True
    

    def update_board(self, x, y):
        """
            Method update_board checks if tiles should swap or if
            game is won/lost.
            Parameters:
                x (float): x coordinate of click
                y (float): y coordinate of click
        """
        if self.quit.clicked_in_region(x, y): # quit
            self.quit_button()
        elif self.load.clicked_in_region(x, y): # load
            self.load_button()
        elif self.reset.clicked_in_region(x, y): # reset
            self.reset_button()
        elif self.check_if_clicked(x, y)[1]:
            if self.moves >= self.moves_allowed:
                # save and sort leaderboard without adding new names
                gameboard.sort_leaderboard(self.leaders)
                gameboard.save_leaderboard(self.leaders)
                self.show_message("Resources/lose.gif")
                self.screen.bye()
            self.swap_tiles(x, y)
            if self.check_solved():
                # update leaders, sort, and save
                self.leaders.append((self.moves, self.name))
                gameboard.sort_leaderboard(self.leaders)
                gameboard.save_leaderboard(self.leaders)
                self.show_message("Resources/winner.gif")
                self.screen.bye()


    def show_message(self, image):
        """
            Method show_message prints chosen message on
            screen.
            Parameters:
                image (str): name of .gif image to show
        """
        tr = turtle.Turtle()
        tr.hideturtle()
        tr.penup()
        tr.setposition(0,0)
        self.screen.addshape(image)
        tr.shape(image)
        tr.showturtle()
        time.sleep(5)
        tr.hideturtle()
        

    ###########################
    #         Buttons         #
    ###########################
    def reset_button(self):
        """
            Method reset resets tile position to winning tiles
        """
        # resets gameboard to unscrambled tile list
        for i in range(len(self.tiles)):
            self.tiles[i].reset()
            


    def load_button(self):
        """
            Method load_button prompts user for a new puzzle to load
            and loads their selection.
        """
        puzzle = self.screen.textinput("Load","""Choose the Puzzle to load:
fifteen.puz
luigi.puz
mario.puz
smiley.puz
yoshi.puz""")
        try:
            # load new tiles
            self.tiles = self.add_puzzle(self.tr, self.screen, puzzle, True)
            # Set board positions (row, col) for new shuffled tiles
            self.set_tile_position(self.tiles)
            # reset moves to 0
            self.moves = 0
            self.tr2.clear()
        except FileNotFoundError:
            self.logger.error(f"{puzzle} file not found LOCATION: board.load_button()")
            self.show_message("Resources/file_error.gif")          


    def quit_button(self):
        """
            Method quit_button quits the game
            and runs the end credits.
        """
        self.show_message("Resources/quitmsg.gif")
        self.show_message("Resources/credits.gif")
        self.screen.bye()

                
    ###########################
    #      Board Set up       #
    ###########################
    def add_puzzle(self, tr, screen, puzzle_file, clear_tiles): 
        """
            Function add_puzzle adds the puzzle to the gameboard
            Parameters:
                tr: turtle used
                screen: screen used
                puzzle_file: .puz file to load
                clear_tiles: bool to check if old tiles need to be cleared
        """
        try:
            # import picture tiles into list - process .puz file and place tiles in a list 
            puzzle = process_puzzle.process_file(puzzle_file, tr, screen)

            is_viable_number = puzzle["number"] == '4' or puzzle["number"] == '9' or \
                                  puzzle["number"] == '16'

            # checks if number is 4, 9, or 16
            if is_viable_number:
                # creates tiles slightly bigger than actual image
                self.size = int(puzzle["size"]) + 2 
                tile_list = puzzle["tiles"]

                try:
                    # add images to screen
                    for i in range(len(puzzle["tiles"])):
                        screen.addshape(puzzle["tiles"][i][1])
                except Exception:
                    self.logger.error(".gif file not found LOCATION: \
board.add_puzzle()")


                if clear_tiles: # clear old puzzle, if applicable
                    self.clear_puzzle()

                
                # randomize and create tiles - load on screen
                random_tiles = self.create_tiles(puzzle, True, True)
            else:
                self.logger.error("Invalid number in .puz file \
LOCATION: board.add_puzzle()")
                self.show_message("Resources/file_error.gif")

            # load thumbnail
            screen.addshape(puzzle["thumbnail"])
            self.thumbnail = Tile(puzzle["thumbnail"], 0, 0, 0, 325, 275,
                                  "none", 0, False, True)
        except FileNotFoundError:
            self.show_message("Resources/file_error.gif")
            self.logger.error(f"Puzzle {puzzle_file} not found \
LOCATION: board.add_puzzle()")
        except KeyError:
            self.logger.error("dictionary key error, \
LOCATION: board.add_puzzle()")
        # return shuffled tiles if dict fully loaded and number is viable
        if is_viable_number: # and len(puzzle) > 5:
            return random_tiles


    def create_tiles(self, puzzle, draw, stamp):
        """
            Method create_tiles takes tiles from file and makes tile instances.
            Parameters:
                puzzle (dict): dictionary of puzzle info to load
                draw (bool): True if drawing tile on screen
                stamp (bool): True if stamping tile on screen
        """
        tiles_per_line = int(math.sqrt(int(puzzle["number"])))
        size = int(puzzle["size"]) + 2  # creates tiles slightly bigger than actual image
        # top left corner of gameboard
        x = -365
        y = 290 

        unshuffled_list = puzzle["tiles"] # create list of tiles to shuffle
        tile_list = process_puzzle.randomize(unshuffled_list) # randomize tiles
        tiles = []
        n = 0
        # Add tiles on to screen: i = rows, j = columns
        for i in range(tiles_per_line):
            for j in range(tiles_per_line):
                orig_image = puzzle[str(n + 1)] # set winning tile image
                tiles.append(Tile(tile_list[n][1], tile_list[n][0], size, size,
                            x + (j * size), y - (i * size), orig_image, (n + 1),
                                  draw, stamp))
                n += 1 # increment index
        return tiles


    def add_buttons(self, buttons):
        """
            Method add_buttons adds non-gameboard tiles to the Board class.
            Parameters:
                buttons (list): list of buttons to be added
            returns list of buttons added
        """
        self.quit = buttons[0]
        self.load = buttons[1]
        self.reset = buttons[2]

    

    def track_player_moves(self, turtle, screen): 
        """
            Method track_player_moves tracks player moves during game
            Parameters:
                turtle (turtle): turtle to set up status line
                screen (screen): Screen to add status line to
                moves (int): Number of moves taken
        """
        self.moves += 1 # increment moves
        turtle.clear()
        turtle.penup()
        turtle.width(2)
        turtle.color("black")
        turtle.setposition(-350, -275)
        turtle.pendown()
        # display on screen
        turtle.write(f"Player Moves: {self.moves}", font =('Arial', 48, 'normal'))


    def clear_puzzle(self):
        """
            Method clear_puzzle clears old puzzle to allow new one
            to be loaded.
        """
        # clear old tiles and thumbnails and hide turtle (if applicable)
        for tile in self.tiles:
            tile.get_tr().clear()
            tile.get_tr().clearstamps()
            self.screen.delay(5)
        self.thumbnail.get_tr().clearstamps()
        self.tr.hideturtle()

