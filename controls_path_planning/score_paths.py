"""
A simple file for scoring paths and producing a summary set of statistics
"""
import typing

import matplotlib.pyplot as plt
import numpy as np
import yaml
from map_info import Destination, MapInfo


def is_keepout_valid(map_info: MapInfo, path: typing.List["tuple"]) -> bool:
    """
    A function to check a path for any incursions into a keepout zone.
    This will check all "steps" on the path and make sure they do not
    occur inside of a keepout zone.

    Note: This means destinations inside of keepouts should always be unreachable
    """
    return all(
        [map_info.risk_zones[int(coord[0])][int(coord[1])] < MapInfo.KEEP_OUT_VALUE for coord in path]
    )


def is_geometry_valid(path: typing.List["tuple"]) -> bool:
    """
    All paths must be 8-connected valid. Each step may only move one cell on
    an 8-connected raster.
    """
    path_steps = np.diff(path, axis=0)
    return np.all(np.logical_or(path_steps == 0, np.abs(path_steps) == 1))


def is_keepin_valid(map_info: MapInfo, path: typing.List["tuple"]) -> bool:
    """
    All paths must stay inside of the "keepin", represented by the edge of the
    risk_zones raster.
    """
    return all(
        [
            all([coord[0] >= 0 for coord in path]),
            all([coord[0] <= map_info.risk_zones.shape[0] for coord in path]),
            all([coord[1] >= 0 for coord in path]),
            all([coord[1] <= map_info.risk_zones.shape[1] for coord in path]),
        ]
    )


def get_path_length(path: typing.List["tuple"]) -> int:
    """
    A small helper function to compute path length
    """
    path_steps = np.diff(path, axis=0)
    return np.sum(np.linalg.norm(path_steps, axis=1))


def get_results(map_info: MapInfo, destinations_with_paths: typing.List["Destination"]) -> str:
    results_dict = dict()
    for site in destinations_with_paths:
        errors = []
        if len(site.path) == 0:
            errors.append("No path to site")
            site_results = dict()
            site_results["errors"] = errors
            site_results["valid"] = False
            site_results["risk"] = np.inf
            site_results["length"] = np.inf
            results_dict[f"{site.site_id}: {site.name}"] = site_results
            continue

        locations_valid = all([all([isinstance(c, int) for c in coord]) for coord in site.path])
        if not locations_valid:
            errors.append("Not all path elements are integers")

        # check to make sure the path starts and ends at start point and destination
        if not site.path[0] == map_info.start_coord:
            errors.append("Path does not start at start coordinates")

        if not site.path[-1] == site.coord:
            errors.append("Path does not end at site coordinates")

        # now check properties of the path itself
        if not is_keepout_valid(map_info, site.path):
            errors.append("Path enters keep out zone")

        if not is_geometry_valid(site.path):
            errors.append("Path steps do not fall on an 8 connected grid")

        if not is_keepin_valid(map_info, site.path):
            errors.append(
                "Path exits the bounds of risk map. Be sure that path coordinates are specified in (south, east) order"
            )

        path_length = get_path_length(site.path)
        if not path_length <= map_info.maximum_range:
            errors.append(
                "Path length ({}) is above maximum range of the zip ({})".format(
                    path_length, map_info.maximum_range
                )
            )

        if is_keepin_valid(map_info, site.path):
            total_risk = sum(
                map_info.risk_zones[int(coord[0])][int(coord[1])] == MapInfo.HIGH_RISK_VALUE
                for coord in site.path
            )
        else:
            total_risk = np.inf

        site_results = dict()
        site_results["length"] = float(path_length)
        site_results["risk"] = float(total_risk)
        valid = len(errors) == 0
        if valid:
            site_results["valid"] = True
        else:
            site_results["errors"] = errors
            site_results["valid"] = False

        results_dict[f"{site.name}"] = site_results

    with open("results.yaml", "w") as results_file:
        yaml.dump(results_dict, results_file)

    results_str = "{}/{} sites reached validly ".format(
        sum(site_result["valid"] for site_result in results_dict.values()),
        len(results_dict),
    )

    for site_name, val in results_dict.items():
        results_str += """
{:>15}: (valid: {:>2}, risk: {:.0f}, length: {:.2f})""".format(
            site_name, val["valid"], val["risk"], val["length"]
        )

    total_risk = sum(site_result["risk"] for site_result in results_dict.values())
    results_str += "\nTotal Risk: {}".format(total_risk)

    return results_str


def display_and_save_result_image(map_info: MapInfo, destinations: typing.List["Destination"]) -> None:
    fig = plt.figure()
    ax = fig.add_axes([0.1, 0.1, 0.6, 0.75])
    handles = []

    handles.extend(map_info.display(ax))

    # Plot each destination
    for destination in destinations:
        site_handle = destination.display(ax)
        handles.extend(site_handle)

    # Add titles and labels
    plt.title("{}".format(map_info.name))
    plt.xlabel("East Coordinate")
    plt.ylabel("North Coordinate")
    plt.legend(handles=handles, bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.savefig("results_fig.png")
    plt.show()
