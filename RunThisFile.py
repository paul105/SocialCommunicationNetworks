from UserData import UserData
from Ratings import Ratings
from Movies import Movies
import os
if __name__ == '__main__':
    root_path = 'C:\Users\p\Documents'
    input_files_path = os.path.join(root_path, 'PycharmProjects\SocialCommunicationNetworks\ml-1m')
    output_files_path = os.path.join(root_path, 'PycharmProjects\SocialCommunicationNetworks\ml-1m\output')
    userdata = UserData(input_files_path, output_files_path)
    userdata.prepare_user_data()
    movies = Movies(input_files_path, output_files_path)
    movies.prepare_user_data()
    ratings = Ratings(input_files_path, output_files_path)
    ratings.prepare_user_data()
