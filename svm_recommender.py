import csv
import math
import numpy as np
from sklearn.svm import SVC


class AutoVivification(dict):
    """Implementation of perl's autovivification feature."""

    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value


class ClassifierSVM(object):

    def __init__(self, path):
        self.users = {}
        self.movies = {}
        self.ratings = AutoVivification()
        self.path = path
        self.load_movies()
        self.load_ratings()
        self.load_users()
        self.users_to_calculate = self.users.keys()[0:25]
        self.similarity = AutoVivification()
        self.movies_correlation = AutoVivification()
        self.find_similarities_between_friends()
        self.find_genre_correlation()
        print "after correlation"
        self.x_train_data = AutoVivification()
        self.y_train_data_watched = {}
        self.y_train_data_not_watched = {}
        self.score = []
        self.prepare_train_data()
        self.avg_score = 0
        print "prepared data"
        self.evaluate_classification()
        self.count_avg_score()


    def load_movies(self):
        with open(self.path + 'movies.csv', "rU") as infile:
            r = csv.reader(infile, delimiter=';')
            for row in r:
                if len(row) > 1:
                    self.movies[row[0]] = row[2:(len(row) - 1)]

    def load_ratings(self):
        with open(self.path + 'ratings.csv', "rU") as infile:
            r = csv.reader(infile, delimiter=';')
            for row in r:
                if len(row) > 1:
                    self.ratings[row[0]][row[1]] = row[2]

    def load_users(self):
        with open(self.path + 'users.csv', "rU") as infile:
            r = csv.reader(infile, delimiter=';')
            for row in r:
                if len(row) > 1:
                    self.users[row[0]] = row[1:(len(row) - 1)]

    @staticmethod
    def sum_differences(friend_ratings, ratings, suma=0):
        for i in range(0, (len(ratings))):
            diff = float(ratings[i]) - float(friend_ratings[i])
            suma = suma + abs(diff)
        return suma

    def find_common_movies(self, friend, ranked_movies):
        ranked_movies_friends = set(self.ratings[friend].keys())
        common_movies = ranked_movies.intersection(ranked_movies_friends)
        return common_movies

    def find_ratings_of_common_movies(self, common_movies, friend, user):
        ratings = []
        friend_ratings = []
        for movie in common_movies:
            ratings.append(self.ratings[user][movie])
            friend_ratings.append(self.ratings[friend][movie])
        return ratings, friend_ratings

    def write_similarity(self, friend, friend_ratings, ratings, user):
        if len(ratings) > 0:
            suma = self.sum_differences(friend_ratings, ratings)
            self.similarity[user][friend] = (1 - suma / len(ratings))
        else:
            self.similarity[user][friend] = 0

    def find_similarities_between_friends(self):
        for user in self.users.keys():
            ranked_movies = set(self.ratings[user].keys())
            for friend in self.users[user][4:(len(self.users[user]) - 1)]:
                common_movies = self.find_common_movies(friend, ranked_movies)
                friend_ratings, ratings = self.find_ratings_of_common_movies(common_movies, friend, user)
                self.write_similarity(friend, friend_ratings, ratings, user)

    def find_genre_correlation(self):
        for movie in self.movies.keys():
            for film in self.movies.keys():
                if film != movie:
                    genres_m = set(self.movies[movie])
                    genres_f = set(self.movies[film])
                    count = len(list(genres_f.intersection(genres_m)))
                    if count > 0:
                        self.movies_correlation[movie][film] = float(count) / len(self.movies[movie])

    def get_watched_films_to_predict(self, user):
        user_films = self.ratings[user].keys()
        number_of_watched_films = math.ceil(0.2 * len(user_films))
        self.y_train_data_watched[user] = user_films[:(len(user_films) - 1)]
        return set(user_films), number_of_watched_films

    def get_unwatched_films_to_predict(self, no_of_films, user, user_films):
        unwatched = list(user_films.intersection(set(self.movies.keys())))[0:int(no_of_films)]
        self.y_train_data_not_watched[user] = unwatched

    def prepare_y_train_data(self, user):
        user_films, no_of_films = self.get_watched_films_to_predict(user)
        self.get_unwatched_films_to_predict(no_of_films, user, user_films)

    def append_info_about_films_to_x(self, film, user):
        for movie in self.ratings[user].keys():
            mark = float(self.ratings[user][movie])
            if movie not in self.y_train_data_watched[user]:
                correlation = self.movies_correlation[movie][film]
                if type(correlation) == int and correlation != 0:
                    self.x_train_data[user][film].append(mark * correlation)
                else:
                    self.x_train_data[user][film].append(mark)
            else:
                self.x_train_data[user][film].append(mark)

    def append_similarities_to_x_train_data(self, film, user):
        for friend in self.similarity[user].keys():
                self.x_train_data[user][film].append(self.similarity[user][friend])

    def prepare_x_train_data(self, user):
        for film in self.y_train_data_watched[user]:
            self.x_train_data[user][film] = self.users[user][0:3]
            self.append_info_about_films_to_x(film, user)
            self.append_similarities_to_x_train_data(film, user)

    def prepare_train_data(self):
        for user in self.users_to_calculate:
            self.prepare_y_train_data(user)
            self.prepare_x_train_data(user)

    def evaluate_classification(self):
        for user in self.users_to_calculate:
            print self.y_train_data_watched[user]
            self.y_train_data_watched[user].extend(self.y_train_data_not_watched[user])
            y_data = self.y_train_data_watched[user]
            y_data.sort()
            y_train = []
            x_train = []
            for movie in y_data:
                if movie in self.y_train_data_not_watched[user]:
                    y_train.append(0)
                else:
                    y_train.append(1)
                x_train.append(map(float, self.x_train_data[user][movie]))
            clf = SVC()
            clf.fit(x_train, y_train)
            score = clf.score(x_train, y_train)
            self.score.append(score)
            print "score: ", score

    def count_avg_score(self):
        self.avg_score = sum(self.score)/len(self.score)


if __name__ == '__main__':
    c = ClassifierSVM('C:\\Users\\JAN\\PycharmProjects\\SocialCommunicationNetworks\\ml-1m\\output\\')
    print c.avg_score
