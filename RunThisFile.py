from UserData import UserData
from Ratings import Ratings
from Movies import Movies
if __name__ == '__main__':
    userdata = UserData("E:\Studia\ES\ml-1m", 'E:\Studia\ES\ml-1m\output')
    userdata.prepare_user_data()
    movies = Movies("E:\Studia\ES\ml-1m", 'E:\Studia\ES\ml-1m\output')
    movies.prepare_user_data()
    ratings = Ratings("E:\Studia\ES\ml-1m", 'E:\Studia\ES\ml-1m\output')
    ratings.prepare_user_data()
