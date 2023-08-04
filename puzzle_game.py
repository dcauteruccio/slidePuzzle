
import turtle, math
import process_puzzle, gameboard, time
from Tile import Tile
from Board import Board
import logging


def set_up_puzzle(tr, screen):
    """
        Function set_up_puzzle sets up Turtle Screen with buttons
        and gameboard.
        Parameters:
            tr (turtle): turtle used to set up board
            screen (screen): screen for the gameboard
        Returns list of the tiles for the game.
    """
    
    # initialize screen and show splash
    tr.hideturtle()
    tr.width(6)
    tr.speed(0)

    name, moves_allowed = user_inputs(screen)
    
    # draw gameboard,
    gameboard.draw_rectangle(450, 450, -375, 300, "black", tr)
    # status bar
    gameboard.draw_rectangle(725, 100, -375, -200, "black", tr)
    # leaderboard
    gameboard.draw_rectangle(250, 450, 100, 300, "blue", tr)

    # add graphics
    screen.addshape("Resources/quitbutton.gif")
    screen.addshape("Resources/loadbutton.gif")
    screen.addshape("Resources/resetbutton.gif")
    quit_button = Tile("Resources/quitbutton.gif", 0, 80, 50, 
                                     260, -225, "none", 0, False, True)
    load = Tile("Resources/loadbutton.gif", 0, 80, 80, 
                              155, -210, "none", 0, False, True)
    reset = Tile("Resources/resetbutton.gif", 0, 80, 
                               80, 55, -210, "none", 0, False, True)

    return [quit_button, load, reset], name, moves_allowed


def splash_screen(tr, screen):
    screen.setup(width=875,height=800) #970, 900
    screen.addshape("Resources/splash_screen.gif")
    tr.shape("Resources/splash_screen.gif")

def user_inputs(screen):
    """
        Function user_inputs gets name and number of moves from user.
        Parameters:
            screen: Turtle screen
        Returns tuple of name, number of moves
    """
    name = screen.textinput("Name", "Enter your name: ")
    moves_allowed = screen.numinput("Moves", "Enter number of moves (5 - 200)",
                                    minval = 5, maxval = 200)

    return name, moves_allowed
        

def main():
    """
        Main function drives the files and executes the game.
    """
    # create main turtle, screen
    tr = turtle.Turtle()
    screen = turtle.Screen()

    leaders = gameboard.open_leaderboard(tr, screen)
    # start screen and display splash screen
    splash_screen(tr, screen)
    time.sleep(5)
    
    # user inputs and puzzle set up
    buttons, name, moves_allowed = set_up_puzzle(tr, screen)
    board = Board(tr, screen, "mario.puz", moves_allowed, buttons,
                  name, leaders)
    gameboard.make_leaderboard(tr, screen, leaders)
    

    # on click, execute board actions (swap, buttons)
    screen.onclick(board.update_board)
    screen.mainloop()


if __name__ == "__main__":
    main()
