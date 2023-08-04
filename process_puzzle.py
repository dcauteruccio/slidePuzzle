"""
    CS5001: Fall 2022
    Puzzle Class
    Dominic Cauteruccio    
"""

import random, time

def process_file(file_name, tr, screen):
    """
        Function process_file parses .puz file into a dict
        Parameters:
            file_name (txt): .puz file with metadata
        Returns dictionary with parsed metadata
    """
    puzzle_info = {"tiles": []}
    # open file, parse info
    with open(file_name, "r") as infile:
        for line in infile:
            lst = line.split(": ")
            lst[1] = lst[1].replace("\n", "")
            # creates dictionary. All metadata parsed
            if lst[0].lower() == "name" or lst[0].lower() == "number" or \
                   lst[0].lower() == "size" or lst[0].lower() == "thumbnail":
                puzzle_info[lst[0].lower()] = lst[1]
            else:
                # All tiles placed into one list
                puzzle_info[lst[0]] = lst[1]
                puzzle_info["tiles"].append((int(lst[0]), lst[1]))

    return puzzle_info


def randomize(tiles):
    """
        Function randomize takes an ordered list of tiles and returns
        a new, separate, unordered list of tiles.
        Parameters:
            tiles (list): ordered list of tiles
        Return:
            tiles_copy (list): unordered list of tiles
    """
    tiles_copy = tiles[:] # temp list for ordering
    randomized_tiles = []
    random.shuffle(tiles_copy)

    return tiles_copy
