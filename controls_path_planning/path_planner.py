"""
    This module is your primary workspace. Add whatever helper functions, classes, data structures, imports... etc here.

    We expect most results will utilize more than just dumping code into the plan_paths()
        function, that just serves as a meaningful entry point.

    In order for the rest of the scoring to work, you need to make sure you have correctly
        populated the Destination.path for each result you produce.
"""
import typing
from queue import PriorityQueue

import numpy as np
from typing import Dict

from map_info import Coordinate, Destination, MapInfo


class PathPlanner:
    def __init__(self, map_info: MapInfo, destinations: typing.List["Destination"]):
        self.map_info: MapInfo = map_info
        self.destinations: typing.List["Destination"] = destinations

    def plan_paths(self):
        """
        This is the function you should re-write. It is expected to mutate the list of
        destinations by calling each Destination's set_path() with the resulting
        path as an argument.

        The default construction shows this format, and should produce 10 invalid paths.
        """
        for site in self.destinations:
            # YOUR CODE REPLACES THIS / WILL PLUG IN HERE
            path_array = np.linspace(self.map_info.start_coord, site.coord, 10)
            path_coords = [Coordinate(arr[0], arr[1]) for arr in path_array]

            # Once you have a solution for the site - populate it like this:
            site.set_path(path_coords)