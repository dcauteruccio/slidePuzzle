
import turtle, time, logging


def format_logger(FileName):
    """
        Function format_logger creates the logger with specified
        FileName.
        Parameters:
            FileName (str): file name to save to
    """
    logger = logging.getLogger('logger')
    handler = logging.FileHandler(FileName)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def draw_rectangle(width, height, x, y, color, tr):
    """
        Function draw_rectangle draws a rectangle with given width,
        height, and color with top left corner starting at x, y.
        Parameters:
            width (int): width of rectangle
            height (int): height of rectangle
            x (int): x coordinate of top left corner
            y (int): y coordinate of top left corner
            color (str): color of rectangle
            tr (Turtle): turtle to draw with
    """
    tr.penup()
    tr.setposition(x, y)
    tr.seth(0)
    tr.pendown()
    tr.color(color)
    tr.forward(width)
    tr.right(90)
    tr.forward(height)
    tr.right(90)
    tr.forward(width)
    tr.right(90)
    tr.forward(height)


def make_leaderboard(turtle, screen, leaders):
    """
        Function make_leaderboard creates and updates leaderboard
        Parameters:
            turtle (turtle): turtle to draw leaderboard with
            screen (screen): Screen to draw leaderboard on
    """
    leaders = leaders
    if len(leaders) > 10: # limit leaderboard to top 10
        len_leaderboard = 10
    else:
        len_leaderboard = len(leaders)
    turtle.penup()
    turtle.width(2)
    turtle.color("blue")
    turtle.setposition(125, 275)
    turtle.pendown()
    turtle.write("Leaders:", font =('Arial', 16, 'normal'))
    turtle.penup()
    turtle.setposition(130, 250)
    # write names of leaders and their scores
    for i in range(0, len_leaderboard):
        turtle.setposition(130, 250 - (i+1)*20)
        turtle.pendown()
        turtle.write(f"{leaders[i][0]} : {leaders[i][1]}",
                     font =('Arial', 16, 'normal'))
        turtle.penup()
    # re-center turtle
    turtle.penup()
    turtle.setposition(0, 0)


def open_leaderboard(tr, screen):
    """
        Function open_leaderboard opens leaderboard file and returns
        the list of leaders.
        Parameters:
            tr (turtle): turtle to print leaderboard error
            screen (screen): screen to show error on
    """
    leaders = []
    try:
        with open("leaders.txt", "r") as infile:
            for line in infile:
                line.strip('\n') # removes \n character
                line = line.split(':')
                if len(line) > 1:
                    leaders.append((int(line[0]), line[1]))
        sort_leaderboard(leaders)
    except FileNotFoundError:
        # error logger
        logger = format_logger('5001_puzzle.err')
        logger.error("leaders.txt file not found LOCATION: \
gameboard.open_leaderboard()")
        # re-center turtle
        tr.penup()
        tr.setposition(0, 0)
        screen.addshape("Resources/leaderboard_error.gif")
        tr.shape("Resources/leaderboard_error.gif")
        tr.showturtle()
        time.sleep(3)
    return leaders


def sort_leaderboard(lst):
    """
        Function sort_leaderboard sorts leaderboard in
        ascending using the merge sort method.
        Parameters:
            leaders (list): list of leaders (unsorted)
    """
    if len(lst) <= 1:
        pass
    if len(lst) > 1:
        mid = len(lst) // 2
        left_half = lst[:mid]
        right_half = lst[mid:]

        sort_leaderboard(left_half) # recursively call ourself with each half
        sort_leaderboard(right_half)

        i = 0 # index for left half
        j = 0 # index for right half
        k = 0 # index for original list

        while i < len(left_half) and j < len(right_half): # merge sublist
            if left_half[i][0] <= right_half[j][0]:
                lst[k] = left_half[i]
                i = i + 1
            else:
                lst[k] = right_half[j]
                j = j + 1
            k = k + 1

        # left list
        while i < len(left_half):
            lst[k] = left_half[i]
            i = i + 1
            k = k + 1

        # right list
        while j < len(right_half):
            lst[k] = right_half[j]
            j = j + 1
            k = k + 1
    

def save_leaderboard(leaders):
    """
        Function save_leaderboard saves leaders list to
        leaders.txt.
        leaders (list): list of leaders
    """
    with open("leaders.txt", "w") as outfile:
        for leader in leaders:
            outfile.write(str(leader[0]) + ":" +
                          leader[1].strip() + '\n')
