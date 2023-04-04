import pandas

def generate_database(streaming_services):
    dataframes = []
    for i in streaming_services:
       dataframes.append(pandas.read_csv("space_efficient_" + i + "_titles.csv"))
    return pandas.concat(dataframes)

def filter_movies_and_tv_shows():
    """
    This will be a function to filter out movies or tv shows
    To be written later
    """

def filter_genre():
    """
    This will be a function to filter out genres
    To be written later
    """