import csv
import sys
import pandas as pd
import obj
from util import Node, QueueFrontier, StackFrontier
import time


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

     #some variables
    frontier = []
    explored_set = []
    breaking = False

    #including dataframes to take references
    print("Loading data...")
    df_people = obj.making_df("people", directory)
    df_stars = obj.making_df("stars", directory)
    df_movies = obj.making_df("movies", directory)
    print("Data loaded.")

    #getting Id of the actors
    source_id = obj.actor_id(df_people, input("Name: "))
    if source_id is None:
        sys.exit("Person not found.")
    target_id = obj.actor_id(df_people, input("Name: "))
    if target_id is None:
        sys.exit("Person not found.")
   

    #Start with a frontier that contains the initial state.
    #Initial State - People

    for i in obj.getting_movies(df_stars, source_id):
        frontier.append([(source_id, i)])


    while breaking == False:
    
        if frontier == []:
            solution = None
            breaking = True
        
        else:
            path_taken = frontier[0].copy()
            analize = path_taken[-1]
            movie = analize[1]
            actors_movie = obj.getting_actors_movie(df_stars, movie)
        
            if target_id in actors_movie:
                solution = path_taken
                breaking = True
            else:
                del(frontier[0])
                explored_set.append(analize[0])
                for j in actors_movie:
                    new_movie = j
                    for k in obj.getting_movies(df_stars,new_movie):
                        new_path = path_taken.copy()
                        new_path.append((new_movie, k))
                                                                          
                        if new_path[-1][0] in explored_set:                        
                            pass
                        else:
                            frontier.append(new_path)

    if solution == None:
        print("Not connected.")
    else:
        solution.append((target_id,"end"))
        degrees = len(solution)-1
        print(f"{degrees} degrees of separation.")
        for i in range(degrees):    
            person1 = obj.taking_name_actor(df_people, solution[i][0])
            person2 = obj.taking_name_actor(df_people, solution[i+1][0])
            movie = obj.taking_name_movie(df_movies, solution[i][1])
            print(f"{i+1}: {person1} and {person2} starred in {movie}")


if __name__ == "__main__":
    main()