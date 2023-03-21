import random

# initialize the list with twice as many movies as there are users
def populate_movies_list(movie_list, seen_movies_list, num_people):
    for i in range(2 * num_people):
        movie_list.append(get_rand_movie_for_list(seen_movies_list))
    return movie_list

# generates random movie to pass to list, checking to make sure it is not a duplicate
# random string of integers for now; once database is up this will connect to the database
# future implimentation of certain criteria to generate movies (genre, title, etc) instead of 
# random movies will depend on movie database
# TODO connect functionality with database
def get_rand_movie_for_list(seen_movies_list):
    str = ""
    for i in range(10):
        str += str(random.randint(0,9))
    
    if str in seen_movies_list:
        return get_rand_movie_for_list(seen_movies_list)
    return str

# gets a "random" movie from the list for the user to vote on
# movies that have been in the list for longer are more likely to be picked
def get_movie_for_user(movie_list):
    n = len(movie_list)
    N = int((n+1)*(n/2))
    x = random.randint(0,N-1)
    for i in range(n):
        I = int(n*(i+1) - ((i+1)*(i/2)))
        if (x < I):
            return movie_list[i]
    return movie_list[0]

# removes the specified movie from the list, and replaces it with a new one
def remove_movie(movie_list, seen_movies_list, movie):
    movie_list.remove(movie)
    movie_list.append(get_rand_movie_for_list(seen_movies_list))


