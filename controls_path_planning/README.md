# Risk Aware Planning

This is second of two options for this year's controls coding challenge. This problem is designed to give us an idea of how you think and program. It represents a realistic (albeit simplified) 
version of one part of the tasks our team has to achieve. Through this project you'll get a small taste of what working 
on these problems would be like, and we will get a chance to see what you're capable of!

This problem is not designed to be _easy_, but it is designed to be solvable in a couple
of hours. You may find that you have to do some additional research to come up with an approach 
to the problem, and that's expected. We often have to do research into state of the art methods
to develop our own algorithms, as the autonomous vehicle space is constantly changing and on 
the bleeding edge. Don't overthink it, though – we don't expect a perfect solution!

# The Problem
Our car has been asked to navigate to a destination. However, there are several possible destinations available, and we won't know 
which destination the car has to drive to until the day of the competition in June. All of the information for these destinations, along with
our starting position, is contained in `map_info.yaml`. The only thing missing is the paths to get to those destinations! Thanks
to aggregated information from our HD map of the area, you have also been provided with a "risk map". This map classifies the region
as "low cost", "high cost", or "keep out". 

Your job is to make a path planning algorithm that generates paths from the starting position to each destination that stays out of
"keep out" zones, _minimizes_ entry into "high cost" zones, and gets to the site within the alloted distance. 

# Getting Started

1. Install requirements from requirements.txt (usually this means `pip install -U -r requirements.txt`). There's nothing fancy going on in the starter code, but if you have an incompatible version of numpy or matplotlib, you'll have a tricky time getting the helper code to run.
2. From this directory - Run`python3 test_planner.py`. You should see a plot showing the Risk Map, Start Location, Site Locations, and some (_invalid and risky_) paths to each site. This will write a copy of the plot to `results_fig.png`. This function will also evaluate the path to each site for validity and evaluate the quality of the path.
3. Your task is to replace the function `PathPlanner.plan_path` in `path_planner.py` to plan the "best" paths to all sites. Paths must follow these rules to be considered valid:
    - __Must__ not enter keep out zones, as denoted by a value in the risk map of 2
    - All path locations __must__ be integers
    - All path steps __must__ take place on an 8 connected grid of step size one
    - Paths __must__ stay within the coordinates of the risk map
    - Paths __must__ start at the start point and end at the site
    - Length of path __must__ be less than specified maximum in map_info.maximum_range
    - Paths _should_ minimize the accumulated risk. Accumulated risk is calculated as the total number of risk pixels that path steps end in
4. Once you have written your code, test it with `python3 test_planner.py` again
5. In addition to your source code, please submit an informal description of your algorithm, your thought process behind developing it, a copy of `results_fig.png` with your paths, a copy of `results.yaml`, as well as any other graphics or information that you think will help us understand whats going on with your algorithm!


#### Notes:

- Be careful of the coordinate order! The map stores coordinates in (east/west, north/south) order. The bottom left of the plot corresponds to 0,0 (similar to a mathematical x,y axis).
- Only the path step start and end points are considered (so cutting corners is a valid tactic!)
- Your path planner should try to optimize BOTH length and cost. There may be multiple "good" ways to get from point A to point B. For example if path 1 has cost=0 and length=20 but path 2 has cost=1 but length=10 which one is "better"? What if the maximum distance is only 10?


# Some guiding principles...

- Your answer does not need to be perfect!
- Simple is better than complex
- Readability Counts
- Practicality and pragmatic problem solving trump perfection

# Questions or Issues:
- Contact kasha2@wisc.edu
