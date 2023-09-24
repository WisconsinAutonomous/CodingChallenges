import typing
from collections import namedtuple
from dataclasses import dataclass

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

Coordinate = namedtuple("Coordinate", ["e", "n"])


@dataclass
class MapInfo:
    """
    This is a class for interacting with our Map

    It will store things like the coordinate we start from
        as well as information on destinations.
    """

    LOW_RISK_VALUE = 0
    HIGH_RISK_VALUE = 1
    KEEP_OUT_VALUE = 2

    def __init__(self, config_dict: dict):

        self.name = config_dict["start"]

        self.start_coord = Coordinate(
            e=config_dict["start_coord"]["e_coord"],
            n=config_dict["start_coord"]["n_coord"],
        )

        self.risk_zones = np.load(config_dict["risk_zones_path"])

        self.maximum_range = config_dict["maximum_range"]

    def display(self, ax: plt.Axes):
        # Show the risk map, making sure that the map is in E-N coordinate frame
        im = plt.imshow(self.risk_zones.T, cmap="Blues", origin="lower")

        # Set legend entries to match the map color scheme
        risk_values = [
            MapInfo.LOW_RISK_VALUE,
            MapInfo.HIGH_RISK_VALUE,
            MapInfo.KEEP_OUT_VALUE,
        ]
        risk_colors = [im.cmap(im.norm(value)) for value in risk_values]
        handles = []
        handles.append(mpatches.Patch(color=risk_colors[0], label="Low Risk"))
        handles.append(mpatches.Patch(color=risk_colors[1], label="High Risk"))
        handles.append(mpatches.Patch(color=risk_colors[2], label="Keep Out"))

        # Plot the start location as a red triangle
        start_handle = plt.plot(*self.start_coord, "r^", markersize=10, label="Start Location")
        handles.extend(start_handle)
        return handles


class Destination:
    def __init__(self, e: int, n: int, site_id: int, name: str):
        self.coord = Coordinate(e=e, n=n)
        self.site_id = site_id
        self.name = name
        self.path = []
        color_list = plt.rcParams["axes.prop_cycle"].by_key()["color"]
        self.color = color_list[self.site_id % len(color_list)]

    def set_path(self, path: typing.List["Coordinate"]) -> None:
        for coord in path:
            if not isinstance(coord, Coordinate):
                raise ValueError(
                    f"""
            The path you are trying to set for site {self.name} is of an invalid type.
            You need to provide a list of type Coordinate.

            The first invalid type in the path was: {coord}
            Full path: {path}
            """
                )
        # if execution makes it here, we have a valid path type.
        self.path = path

    def display(self, ax: plt.Axes):
        if len(self.path) > 0:
            e_coords = [coord.e for coord in self.path]
            n_coords = [coord.n for coord in self.path]
            plt.plot(e_coords, n_coords, ".-", color=self.color)
            handle = ax.plot(*self.coord, "o", color=self.color, label=f"{self.site_id}: {self.name}")
        else:
            handle = ax.plot(
                *self.coord,
                "rx",
                color=self.color,
                label=f"{self.site_id}: {self.name}",
            )
        return handle


def load_destinations(config_dict: dict) -> typing.List["Destination"]:
    destinations = []
    for site_info in config_dict.get("destinations", []):
        site = Destination(
            e=site_info["e_coord"],
            n=site_info["n_coord"],
            site_id=site_info["site_id"],
            name=site_info.get("name"),
        )
        destinations.append(site)
    return destinations
