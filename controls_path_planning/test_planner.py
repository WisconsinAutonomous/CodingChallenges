import argparse

import yaml
from map_info import MapInfo, load_destinations
from path_planner import PathPlanner
from score_paths import display_and_save_result_image, get_results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""
        This is the main runner for testing and iterating on your path planner.

        It takes a single optional argument - the problem definition file.
        The default problem definition file contains a start, some destinations, and some important
        parameters for the paths you plan.

        This runner will load the default data classes, and pass them into the
        PathPlanner object for use. It will call the plan_paths function, which
        you are expected to implement.

        After the function completes, destinations that have been planned to
        should have their paths stored on the Destination object passed into the
        PathPlanner object.

        Summary results will be printed to your terminal, and a results.yaml file
        will be produced and written to this directory.

        A visual of routes planned will also be produced. The default form of this
        should show straight, invalid paths to the Destination.
        """,
    )
    parser.add_argument("--map-info-path", required=False, type=str, default="map_info.yaml")
    args = parser.parse_args()

    with open(args.map_info_path) as file:
        config_dict = yaml.load(file, Loader=yaml.FullLoader)

    # load the data problem definition into MapInfo and our destinations
    map_info = MapInfo(config_dict)
    destinations = load_destinations(config_dict)

    # construct the path planner object
    path_planner = PathPlanner(map_info, destinations)

    # kick off path planning now that everything is loaded
    path_planner.plan_paths()

    # show the results in the terminal, and save to disk
    print(get_results(map_info, destinations))
    display_and_save_result_image(map_info, destinations)
