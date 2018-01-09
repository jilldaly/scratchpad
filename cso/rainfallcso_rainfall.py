#!/usr/bin/env python3
"""
@author: Jill Daly

Assumptions:
    - that the .txt files are in the same directory as this python program
    - that statistics are displayed with a .2 decimal place
    - that the data files columns are in this order:
          Year, Month, Total Rainfall, Most Rainfall, Rain days
"""
import numpy as np
from sys import exit

# Gobals used for our Singleton pattern for the data
global_counties_dict = None
global_counties_data_dict = None


def get_counties_dict():
    """
    The index/position of each county is closely coupled with the order in
    which data is retrieved and displayed. We need to restrict this ordering to
    have a single source of truth, so that we can ensure the accuracy of the
    data being displayed.

    This reduces duplicated code and hardcoded ordering, which follows the
    principles outlined by programming best practices (see https://12factor.net)
    """
    global global_counties_dict
    # use the global countiesDict to store the option -> county as a key -> value
    if global_counties_dict is None:
        global_counties_dict = {"1": "Cork", "2": "Belfast", "3": "Dublin", "4": "Galway", "5": "Limerick"}

    return global_counties_dict


def load_rainfall_txt_files():
    """
    We only want to load the county Data files once, so as to save on
    performance and memory. This function is a version of the singleton
    pattern so that we re-use the dict after its been initialised
    """
    global global_counties_data_dict
    if global_counties_data_dict is None:
        # use the global countiesDict to store the numpy data arrays
        global_counties_data_dict = dict()
        for k, v in sorted(get_counties_dict().items()):
            global_counties_data_dict[v] = np.genfromtxt(v + "Rainfall.txt", dtype=float, delimiter=' ')

    return global_counties_data_dict


def ask_for_int(prompt, retries=2, reminder='Please try again!'):
    """
    Safely Retrieves an int from a user input, allowing the user to correct a
    non-int mistake.

    After several attempts, an error message will be displayed, and the program
    will exit
    """
    while True:
        try:
            return int(input(prompt))
        except:
            pass

        retries = retries - 1
        if retries < 0:
            print('Invalid number, unable to continue')
            exit()

        print(reminder)


def basic_stats_by_location(message, dataIndex):
    """
    Display a menu to the user, showing each dict k,v as an option
    numbered-location.
    Using the number entered, load the relevant file and return the location
    and numpy data array
    """
    counties_dict = get_counties_dict()
    for k, v in sorted(counties_dict.items()):
        print(f"{k}. {v}")

    loc_choice = input("Please select a location: ")
    if loc_choice not in counties_dict:
        print(f"There is currently no option '{loc_choice}' available")
        return

    loc = counties_dict[loc_choice]
    data_dict = load_rainfall_txt_files()

    print()
    print(f"{loc}: Max {message} = {np.amax(data_dict[loc], axis=0)[dataIndex]:.2f}")
    print(f"{loc}: Average {message} = {np.mean(data_dict[loc], axis=0)[dataIndex]:.2f}")


def cumulative_stats(start, end):
    """
    For the given start and end index values for the relevant columns, return a
    cumulative numpy data array
    """
    data_dict = load_rainfall_txt_files()
    counties_data_list = list()
    for k, v in sorted(get_counties_dict().items()):
        counties_data_list.append(data_dict[v][:, start:end])

    return np.concatenate(counties_data_list, axis=1)


def print_cum_stats(cum_totals, unit):
    """
    Print out the relevant Cumulative Stats for each County
    """
    for k, v in sorted(get_counties_dict().items()):
        print(f"{k}. {v} {cum_totals[int(k)-1]:0.2f}{unit}")


def calc_total_rainfall():
    """
    Calculate and display the Max and Avg Total Rainfall for a selected location
    """
    basic_stats_by_location("Total Rainfall", 2)


def calc_most_rainfall():
    """
    Calculate and display the Max and Avg Total Rainfall for a selected location
    """
    basic_stats_by_location("Most Rainfall in a Day", 3)


def calc_num_rain_days():
    """
    Calculate and display the Max and Avg Total Rainfall for a selected location
    """
    basic_stats_by_location("Number of Rain days", 4)


def calc_wettest_loc():
    """
    Calculate and display the the cumulative Total Rainfall stats for all locations
    """
    counties = sorted(get_counties_dict().items())

    # Calculate cumulative stats for Total rain, and display results
    cum_array = cumulative_stats(2, 3)
    cum_totals = np.sum(cum_array, axis=0)
    print_cum_stats(cum_totals, "mm")

    # Display the stat for the max county
    row_index = np.argmax(cum_totals, axis=0)
    print()
    print(
        f"The wettest location in Ireland is {counties[row_index][1]} with a rainfall figure of {cum_totals[row_index]:.2f}mm")


def calc_prob_rain_days():
    """
    Calculate and display the the cumulative Probability Rainfall stats for all
    locations, taking into account the 'days' threshold provided by user
    """
    # Retrieve the Number data for all counties
    cum_array = cumulative_stats(4, 5)

    # Retrieve the threshold from the user, and filter the cumulative array for
    # each county. Filter by the threshold provided by the user
    days = ask_for_int("Please enter maximum threshold value for number of rain days:")
    cum_day_list = list()
    for k, v in sorted(get_counties_dict().items()):
        # index is -1 from the key
        county_array = cum_array[:, int(k) - 1:int(k)]
        bool_array = county_array <= days
        cum_day_list.append((len(county_array[bool_array]) * 100.0 / len(county_array)))

    # Display the probability stats for each county using our cumulative list
    # and % unit of measurement
    print_cum_stats(cum_day_list, "%")


def main():
    """
    Present the main menu to the user, and execute the relevant choice/function
    """
    # Create the choice -> function mapping in a dict
    main_menu = {
        "1": ("Most successful directors or actors", calc_total_rainfall),
        "2": ("Basic Statistics for Most Rainfall in a Day (Millimetres)", calc_most_rainfall),
        "3": ("Analyse the distribution of gross earnings", calc_num_rain_days),
        "4": ("Wettest Location", calc_wettest_loc),
        "5": ("Percentage of Rain Days", calc_prob_rain_days),
        "6": ("Exit", None)
    }

    # Loop through the main menu of choices, until the user selects Exit
    while True:
        print("\nPlease select one of the following options:\n")
        for k, v in sorted(main_menu.items()):
            print("{}  {}".format(k, v[0]))

        choice = input("\n> ")
        if choice in main_menu:

            # Before we call our functions, check if the user selected Exit
            if "6" == choice:
                print('Exiting the application')
                break

            main_menu[choice][1]()
        else:
            print("No such option.")


# call the main method to start the program
main()
