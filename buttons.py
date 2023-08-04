
import turtle
from Tile import Tile
from process_puzzle import process_file


def add_button(image, fun, x, y, screen):
    """
        Function add_button adds the appropriate button to gameboard
        Parameters:
            image (str): image file for button
            fun (function): function with button functionality
            x (float): x coordinate of button placement
            y (float): y coordinate of button placement
            screen (screen): screen to place button on
        Return turtle representing the button
    """
    # set turtle to an image, move to it's spot, and add the function
    # to pass in to perform onclick
    tr = turtle.Turtle()
    tr.speed(0)
    tr.penup()
    tr.setposition(x, y)
    try:
        screen.addshape(image)
    except FileNotFoundError:
        raise FileNotFoundError
    tr.shape(image)

    tr.onclick(fun)

    return tr


def load_puzzle(screen):
    """
        Function load_puzzle loads puzzle user chooses from list.
        Parameters:
            screen: Turtle Screen
        Return puzzle to be opened
    """
    
    puzzles = ["fifteen.puz", "luigi.puz", "mario.puz", "smiley.puz", "yoshi.puz"]
    puzzle = screen.textinput("""Choose the Puzzle to load:
fifteen.puz
luigi.puz
mario.puz
smiley.puz
yoshi.puz""")
    
    return process_file(puzzle)


def reset(puzzle):
    pass

def quit(screen):
    """
        Function quit lets user game when user clicks the quit button.
    """
    pass #screen.done()
    
