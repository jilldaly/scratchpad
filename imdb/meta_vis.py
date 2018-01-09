#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Jill Daly
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import make_classification


def ask_for_int(prompt, retries=100, reminder='Please try again!'):
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
 
    
    
def ask_for_display_count(upper_limit, item_type):
    """
    Validates user input for count integer entered
    """
    # get the user input for number of items to display
    while True:
        count_choice = ask_for_int(f"Please specify the number of {item_type} to display:")
                
        if ((count_choice > 0) and (count_choice < upper_limit)):
            break
        else:
            print('Amount choice not within bounds of', 0, 'and', upper_limit)  
            
    return count_choice

       
        
def most_successful(df):    
    """
    Asks the user to chooose between Most Successful Director and 
    Most Successful Actor.
    """
    # Offer the User the choices available
    print('\ni.  Top Directors')
    print('ii. Top Actors')
    
    # Allow the user to enter their choice in a user friendly manner
    while True:
        choice = input('Please select either i or ii: ')
    
        if choice == 'i' or choice == 'ii':
            break
        else: 
            print('Unable to read', choice)
            
    # Call the relevant display function based on the selected choice        
    if choice == 'i':
        most_successful_dir(df)
    else:
        most_successful_actor(df)



def most_successful_actor(df):
    """
    Groups the DataFrame to find the most successful actors and displays 
    this information in a bar chart.
    
    The user is given the option to choose the number of actors to display
    """
    # create a dataframe with just two columns, for simplicity
    df_actor_1 = df[['actor_1_name','gross', 'movie_title']]
    df_actor_2 = df[['actor_2_name','gross', 'movie_title']]
    df_actor_3 = df[['actor_3_name','gross', 'movie_title']]

    df_columns = ['actor_name', 'gross', 'movie_title']
    df_actor_1.columns = df_columns
    df_actor_2.columns = df_columns
    df_actor_3.columns = df_columns
    
    df_actors = pd.concat([df_actor_1, df_actor_2, df_actor_3], ignore_index=True)
    df_actors = df_actors.dropna()
    
    # When we have the data merged, we need to check the upper limit
    actor_count = len(df_actors['actor_name'].unique())
    
    # Ask the user to input how many actors to display
    actor_count_choice = ask_for_display_count(actor_count, 'actors')

    # group the data by director name, creates a Panda Group By Data Frame
    df_by_actor = df_actors.groupby('actor_name', as_index=False)
    df_by_actor = df_by_actor.agg({'gross':np.sum})
    
    df_by_actor = df_by_actor.sort_values(['gross'], ascending=False)
    df_plot = df_by_actor.head(actor_count_choice)
        
    # Print out for the report
    # print(df_plot)
    
    # display the results in a horizontal bar chart
    ax = sns.barplot(x='gross', y='actor_name', data=df_plot, orient="h", color='blue')
    ax.set(xlabel='Gross (in Billions)', ylabel='Actor', 
           title=f'{actor_count_choice} Most Succesful Actors')
    plt.show()
   
    
    
def most_successful_dir(df):
    """
    Groups the DataFrame to find the most successful directors and displays 
    this information in a bar chart.
    
    The user is given the option to choose the number of directors to display
    """
    # get the number of directors, so that we can validate the user input   
    dir_count = len(df['director_name'].unique())
    
    # Ask the user to input how many directors to display
    dir_count_choice = ask_for_display_count(dir_count, 'directors')
    
    # create a dataframe with just two columns, for simplicity
    df = df[['director_name','gross', 'movie_title']]
    
    # group the data by director name, creates a Panda Group By Data Frame
    df_by_dir = df.groupby('director_name', as_index=False)
    df_by_dir = df_by_dir.agg({'gross':np.sum})
    
    df_by_dir = df_by_dir.sort_values(['gross'], ascending=False)
    df_plot = df_by_dir.head(dir_count_choice)
    
    # Print out for the report
    # print(df_plot)
    
    # display the results in a horizontal bar chart
    ax = sns.barplot(x='gross', y='director_name', data=df_plot, orient="h", color='blue')
    ax.set(xlabel='Gross (in Billions)', ylabel='Director', 
           title=f'{dir_count_choice} Most Succesful Directors')
    plt.show()



def film_comparison(df):
    """
    Allows the user to compare films based on Gross Earnings, IMDB Scores, or
    Movie Facebook Likes
    
    """
    # First, get the list of movies that are available in the dataset
    movies_menu = df['movie_title'].unique()
    
    # Then, allow the user to successfully enter two valid movies to compare    
    movie_choice1 = input('Please Enter the first film to compare: ' )
    movie_choice2 = input('Please Enter the second film to compare: ')    
    while True:
        if movie_choice1 not in movies_menu:
            movie_choice1 = input('Your first movie choice is not available, please choose again: ')
            continue
        
        if movie_choice2 not in movies_menu:
            movie_choice2 = input('Your second choice is not available, please choose again: ')
            continue
        
        if (movie_choice1 in movies_menu) and (movie_choice2 in movies_menu):
            break
        
    # Once the movies are selected, next we get the comparison data
    df_comparison = df[((df['movie_title'] == movie_choice1 ) | (df['movie_title'] == movie_choice2))]
    df_comparison = df_comparison[['movie_title', 'gross', 'movie_facebook_likes', 'imdb_score']]
    
    # Offer the User the choices available
    print('\ni.   IMDB Scores')
    print('ii.   Gross Earnings')
    print('iii.   Movie Facebook Likes')
    
    # Allow the user to enter their choice in a user friendly manner
    while True:
        choice = input('Please select either i, ii or iii: ')
    
        if choice == 'i' or choice == 'ii' or choice == 'iii' :
            break
        else: 
            print('Unable to read', choice)
            
    
    # Call the relevant display function based on the selected choice        
    if choice == 'i':
        imdb_scores(df_comparison)
    elif choice == 'ii':
        gross_earnings(df_comparison)
    else:
        movie_fb_like(df_comparison)
    
    
    
def imdb_scores(df):
    """
    Display a bar chart comparing movies IMDB scores
    """  
    ax = sns.barplot(x='imdb_score', y='movie_title', data=df, orient="h", color='blue')
    ax.set(xlabel='IMDB Scores', ylabel='Movie', title='IMDB Scores Comparison')
    plt.show()
    
    
    
def gross_earnings(df):
    """
    Display a bar chart comparing movies gross earnings
    """
    ax = sns.barplot(x='gross', y='movie_title', data=df, orient="h", color='blue')
    ax.set(xlabel='Gross (in Billions)', ylabel='Movie', title='Movie Gross Earnings Comparison')
    plt.show()



def movie_fb_like(df):
    """
    Display a bar chart comparing movies facebook likes
    """    
    ax = sns.barplot(x='movie_facebook_likes', y='movie_title', data=df, orient="h", color='blue')
    ax.set(xlabel='Facebook Likes', ylabel='Movie', title='Movie Facebook Likes Comparison')
    plt.show()



def dist_gross_earnings(df):
    """
    Allows the user to successfully enter a date range to compare the 
    distribution statistics for the Gross Earnings per anum. 
    Displays a line chart for Average, Min and Max values per year
    
    """    
    df_dist = df[['title_year', 'gross']]

    # allow the user to successfully enter two years to analyse    
    min_yr = int(np.min(df_dist[['title_year']])[0])
    max_yr = int(np.max(df_dist[['title_year']])[0])
    print(f'\nThe range of Years to choose from are {min_yr} to {max_yr}')
    yr_start = ask_for_int('Please Enter the start year for distribution analysis: ' )
    yr_end = ask_for_int('Please Enter the end year  for distribution analysis: ')    
    while True:
        if min_yr > yr_start:
            yr_start = ask_for_int('Your start year is out of range, please enter a new value: ')
            continue
        
        if yr_start >= yr_end:
            print('The year end must be at least one year after the year start')
            yr_start = ask_for_int('Please Enter the start year for distribution analysis: ' )
            yr_end = ask_for_int('Please Enter the end year  for distribution analysis: ')    
            continue
        
        if yr_start < yr_end:
            break    
    
    
    df_dist = df_dist[((df.title_year >= yr_start)  & (df.title_year <= yr_end))]
    
    df_by_year = df_dist.groupby('title_year', as_index=False)
    df_by_year_min_gross = df_by_year.agg({'gross':np.min})
    df_by_year_min_gross = df_by_year_min_gross.rename(columns={'gross': 'min_gross'})
    df_by_year_max_gross = df_by_year.agg({'gross':np.max})
    df_by_year_max_gross = df_by_year_max_gross.rename(columns={'gross': 'max_gross'})
    df_by_year_mean_gross = df_by_year.agg({'gross':np.mean})
    df_by_year_mean_gross = df_by_year_mean_gross.rename(columns={'gross': 'avg_gross'})
    
    df_merged = pd.merge(df_by_year_min_gross, 
                         df_by_year_max_gross,
                         on='title_year',
                         how='inner')
    df_merged = pd.merge(df_merged, 
                         df_by_year_mean_gross,
                         on='title_year',
                         how='inner')
    
    plot_title = f'Avg, Min, and Max Gross Earnings from {yr_start} to {yr_end}'
    
    ax = df_merged.plot(x='title_year', y=['min_gross', 'max_gross', 'avg_gross'], kind='line')
    ax.set(xlabel='Year', ylabel='Movie Gross (in Billions)', 
           title=plot_title)
    ax.legend(labels=('Min Gross', 'Max Gross', 'Avg Gross'))
    plt.show()
    
    

def genre_analysis(df):
    """
    Allows the user to enter a specific genre from the availble genres, and then
    displays the mean IMDB score for the chosen genre. 
    """
    # parse the dataframe for available genres
    genre_series = df['genres'].str.split('|').apply(pd.Series).stack().reset_index(drop=True)    
    genre_unique = genre_series.unique()
    
    # Display the options available to the user
    print('\nThe following are the available genres:\n')
    print("\n".join(genre_unique))
    
    # Allow the user to successfully choose a genre
    while True:        
        genre = input('\nPlease enter your chosen genre: ')
        if genre in genre_unique:
            break
        else:
            print('No match found for', genre)
    
    # calculate and display the mean IMDB score for the chosen genre
    mean_imdbscore = round(np.mean(df[df['genres'].str.contains(genre)]['imdb_score']), 4)
    print(f'\nAverage IMDB Score for {genre} films is: {mean_imdbscore}')
        
    

def earnings_and_scores(df):
    """
    Visualise the relationship between the label value IMDB Score and the other
    Continuous features
    """    
    print('Building charts...')
    
    df1 = df[["imdb_score",
              "gross",
              "budget",
              "num_voted_users",
              "director_facebook_likes",
              "movie_facebook_likes",
              "cast_total_facebook_likes",
              "num_critic_for_reviews",
              "num_user_for_reviews"]]


    ax1 = sns.lmplot(x='gross', y='imdb_score', data=df1)
    ax1.set(xlabel='Gross (in Billions)', ylabel='IMDB Scores', 
           title=f'Linear Relationship for Gross Earnings (Billions)v IMDB Scores')
    
    ax2 = sns.lmplot(x='budget', y='imdb_score', data=df1)
    ax2.set(xlabel='Budget (in Billions)', ylabel='IMDB Scores', 
           title=f'Linear Relationship for Budget (Billions) v IMDB Scores')
    
    ax3 = sns.lmplot(x='num_voted_users', y='imdb_score', data=df1)
    ax3.set(xlabel='Number Votes', ylabel='IMDB Scores', 
           title=f'Linear Relationship for Number Votes v IMDB Scores')
    
    ax4 = sns.lmplot(x='director_facebook_likes', y='imdb_score', data=df1)
    ax4.set(xlabel='Director Facebook Likes', ylabel='IMDB Scores', 
           title=f'Linear Relationship for Director Facebook Likes v IMDB Scores')
    
    ax5 = sns.lmplot(x='movie_facebook_likes', y='imdb_score', data=df1)
    ax5.set(xlabel='Movie Facebook Likes', ylabel='IMDB Scores', 
           title=f'Linear Relationship for Movie Facebook Likes v IMDB Scores')
    
    ax6 = sns.lmplot(x='cast_total_facebook_likes', y='imdb_score', data=df1)
    ax6.set(xlabel='Cast Total Facebook Likes', ylabel='IMDB Scores', 
           title=f'Linear Relationship for Cast Total Facebook Likes v IMDB Scores')
    
    ax7 = sns.lmplot(x='num_critic_for_reviews', y='imdb_score', data=df1)
    ax7.set(xlabel='Num Critics for Review', ylabel='IMDB Scores', 
           title=f'Linear Relationship for Num Critics for Review v IMDB Scores')
    
    ax8 = sns.lmplot(x='num_user_for_reviews', y='imdb_score', data=df1)
    ax8.set(xlabel='Num Users for Review', ylabel='IMDB Scores', 
           title=f'Linear Relationship for Num Users for Review v User reviews')
    
    
    print('\nLinear Regression Charts:')

    plt.show()

    X, y = make_classification(n_samples=len(df1), 
                               n_classes=1, 
                               n_informative=8,  
                               n_redundant=0,
                               random_state=0)
    
    corrResults = df.corr()
    sns.heatmap(corrResults)

    print('Heat Map:')
    plt.show()


    
def clean_data(df):
    """
    """    
    # Store count of rows from the outset (5043)
    #pre_de_dup_count = len(df)

    # drop duplicates
    df_new = df.drop_duplicates()
    
    # Store count after de-duplicating (4998)
    #post_de_dup_count = len(df_new)

    # drop any missing values from specified columns
    df_new = df_new.dropna(subset = ['director_name', 
                                 'actor_1_name', 
                                 'actor_2_name', 
                                 'actor_3_name', 
                                 'gross',
                                 'title_year'])    
    
    # reset the index to clear any gaps from dropped rows due to nas
    df_new = df_new.reset_index(drop=True)

    # Store count after dropping na's for specified columns
    #post_drop_na_count = len(df_new)
  
    # remove any speacial characters from the movie titles
    df_new.movie_title = df_new.movie_title.str.replace('[^\x00-\x7F]','')
    df_new.movie_title = df_new.movie_title.apply(lambda x: x.strip())
    
    return df_new



def main():
    """
    Present the main menu to the user, and execute the relevant choice/function
    """

    # read the csv into a pandas dataframe, de-duplicate and reset the index
    df = pd.read_csv('movie_metadata.csv', encoding='ISO-8859-1')
    df = clean_data(df)


    # Create the choice to function mapping in a dict
    main_menu = {
        "1": ("Most successful directors or actors", most_successful),
        "2": ("Film comparison", film_comparison),
        "3": ("Analyse the distribution of gross earnings", dist_gross_earnings),
        "4": ("Genre Analysis", genre_analysis),
        "5": ("Earnings and IMDB scores", earnings_and_scores),
        "6": ("Exit", None)
    }

    # this line is hardcoded for dev-testing
    # main_menu["5"][1](df)

    # Loop through the main menu of choices, until the user selects Exit
    while True:
        print("\nPlease select one of the following options:\n")
        for k, v in sorted(main_menu.items()):
            print("{}  {}".format(k, v[0]))

        choice = input("\n> ")
        if choice in main_menu:
            
            # Before we call our fucntions, check if the user selected Exit
            if "6" == choice:
                print('Exiting the application')
                break
            
            main_menu[choice][1](df)
        else:
            print("No such option.")




# call the main method to start the program
main()
