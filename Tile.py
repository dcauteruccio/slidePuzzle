"""
    CS5001: Fall 2022
    Tile Class
    Dominic Cauteruccio
"""

import turtle
from gameboard import draw_rectangle

class Tile:
    """
        Tile Class to create individual tiles on the gameboard. Functionality
        includes the ability to swap with another tile and "reset" back to
        it's original location.
    """
    def __init__(self, image, tile_num, width, height,
                 x, y, original_image, original_num, draw, stamp):
        """
            Method __init__ initializes a new instance
            of Puzzle and loads it onto the gameboard.
            Parameters:
                image_tuple (tuple): winngin pos and name of .gif image
                width (int): width of tile
                height (int): height of tile
                x (int): x coordinate of top left corner
                y (int): y coordinate of top left corner
                draw (bool): True if drawing tile on screen
                stamp (bool): True if stamping tile on screen
        """
        self.image = image
        self.tile_number = tile_num
        self.original_number = original_num # winning tile_num
        self.original_image = original_image # winning tile image
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.is_blank_tile = self.is_blank() # check if blank
        
        # turtle set up
        self.tr = turtle.Turtle()
        self.tr.speed(0)
        self.tr.hideturtle()

        if draw:
            draw_rectangle(self.width, self.height, self.x, self.y, \
                           "black", self.tr)
        if stamp:
            self.set_tile_image(self.image) # stamp image
    
    
    # Getter Methods
    def get_image(self):
        """
            Method get_image returns the image of the instance.
        """
        return self.image


    def get_tile_number(self):
        """
            Method get_tile_num returns the tile number
            of the instance.
        """
        return self.tile_number


    def get_original_image(self):
        """
            Method get_original_image returns the
            winning image of the tile.
        """
        return self.original_image
    

    def get_original_number(self):
        """
            Method get_original_number returns the
            winning tile number of the instance.
        """
        return self.original_number
    

    def get_position(self):
        """
            Method get_position returns the x,y coordinates
            of the top left corner of the instance.
        """
        return self.x, self.y


    def get_board_pos(self):
        """
            Method get_board_position returns the row and column
            position of the tile on the board.
        """
        return self.row, self.col


    def get_width(self):
        """
            Method get_width returns the width
            of the tile.
        """
        return self.width


    def get_height(self):
        """
            Method get_height returns the height
            of the tile.
        """
        return self.height


    def get_tr(self):
        """
            Method get_tr returns the turtle
            of the tile.
        """
        return self.tr


    # Setter Methods
    def set_position(self, x, y):
        """
            Method set_position sets the x,y coordinates
            of the top left corner of the instance.
        """
        self.x = x
        self.y = y


    def set_board_pos(self, row, col):
        """
            Method set_board_pos sets the row and column
            position of the tile on the board.
        """
        self.row = row
        self.col = col


    def set_tile_image(self, image):
        """
            Method set_tile_image sets tile image inside given tile.
        """
        # move turtle to center of tile
        self.tr.penup()
        self.tr.setposition(self.x + (self.width / 2),
                            self.y - (self.height / 2))
        self.tr.pendown()

        # stamp image
        self.image = image
        self.tr.shape(image)
        self.tr.stamp()
        self.is_blank() # update if blank bool


    def set_tile_number(self, tile_num):
        """
            Method set_board_pos sets the row and column
            position of the tile on the board.
        """
        self.tile_number = tile_num


    # Boolean methods, checks if something is true
    def is_adjacent(self, other):
        """
            Method checks if tiles are next to each other
        """
        other_row, other_col = other.get_board_pos()
        # if sum of row, col of other within 1 of self, return True
        if abs(other_row - self.row) + \
           abs(other.col - self.col) == 1:
            return True
        else:
            return False


    def is_blank(self):
        """
            Method is_blank checks if tile is blank.
            Returns boolean if blank or not.
        """
        if "blank" in self.image.lower():
            return True
        else:
            return False

    def is_home(self):
        """
            Method is_home checks whether tile is in
            winning tile position
        """
        return self.image == self.original_image and \
               self.tile_number == self.original_number


    def clicked_in_region(self, x, y):
        """
            Method clicked_in_region determines if the tile
            was clicked on during the game.
            Parameters:
                x (float): x coordinate of click
                y (float): y coordinate of click
            Returns True if click was in tile
        """
        # set outer bounds for tile
        lower_x = self.x
        upper_x = self.x + self.width
        lower_y = self.y - self.height
        upper_y = self.y

        # boolean to check if click in tile or not
        in_tile = (x > lower_x and x < upper_x
                    and y > lower_y and y < upper_y)

        if in_tile:
            return True

    
    # Action Methods 
    def swap(self, other):
        """
            Method swap swaps places with another tile.
            Parameters:
                other (tile): tile to swap with
        """
        # check if next to each other and are blank:
        if other.is_adjacent(self) and other.is_blank():
            # swap images
            temp = self.get_image()
            self.set_tile_image(other.get_image())
            other.set_tile_image(temp)
            # swap tile_num
            self_temp = self.get_tile_number()
            self.set_tile_number(other.get_tile_number())
            other.set_tile_number(self_temp)
            # swap board_pos
            #temp_pos = self.get_board_pos()
            #other_pos = other.get_board_pos()
            #self.set_board_pos(other_pos[0], other_pos[1])
            #other.set_board_pos(temp_pos[0], temp_pos[1])
            

    def reset(self):
        """
            Method reset resets tile to original (unshuffled)
            image and tile number.
        """
        self.set_tile_number(self.original_number)
        self.set_tile_image(self.original_image)

