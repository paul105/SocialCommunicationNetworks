from FileCommonGetter import FilecommonGetter
import re


class Movies(FilecommonGetter):
    def __init__(self, src_path, dst_path):
        super(Movies, self).__init__(src_path, dst_path)
        self.file_name = None
        self.movie_id = []
        self.title = []
        self.genres = []

################# user api #####################################################
    def prepare_user_data(self, separator='::'):
        self.prepare()
        self.split_data_in_files(separator=separator)
        self.get_file_name('movie')
        self.split_list_to_separate_list()
        self.split_genres_and_change_to_numbers()
        self.output = self.prepare_output_to_save_to_file(self.movie_id, self.title, genres=self.genres)
        self.save_to_file(self.output, self.file_name)

############### private api #####################################################

    def split_list_to_separate_list(self):
        for index, line in enumerate(getattr(self, self.file_name)):
            self.movie_id.append(line[0])
            self.title.append(line[1])
            self.genres.append(line[2])

    def split_genres_and_change_to_numbers(self):
        for index, line in enumerate(self.genres):
            self.genres[index] = self.genres[index].replace("Action", '0')
            self.genres[index] = self.genres[index].replace("Adventure", '1')
            self.genres[index] = self.genres[index].replace('Animation', '2')
            self.genres[index] = self.genres[index].replace("Children's", '3')
            self.genres[index] = self.genres[index].replace("Comedy", '4')
            self.genres[index] = self.genres[index].replace("Crime", '5')
            self.genres[index] = self.genres[index].replace("Documentary", '6')
            self.genres[index] = self.genres[index].replace("Drama", '7')
            self.genres[index] = self.genres[index].replace("Fantasy", '8')
            self.genres[index] = self.genres[index].replace("Film-Noir", '9')
            self.genres[index] = self.genres[index].replace("Horror", '10')
            self.genres[index] = self.genres[index].replace("Musical", '11')
            self.genres[index] = self.genres[index].replace("Mystery", '12')
            self.genres[index] = self.genres[index].replace("Romance", '12')
            self.genres[index] = self.genres[index].replace("Sci-Fi", '13')
            self.genres[index] = self.genres[index].replace("Thriller", '14')
            self.genres[index] = self.genres[index].replace("War", '15')
            self.genres[index] = self.genres[index].replace("Western", '16')
            self.genres[index] = self.genres[index].split("|")

if __name__ == '__main__':
    movies = Movies("E:\Studia\ES\ml-1m", 'E:\Studia\ES\ml-1m\output')
    movies.prepare_user_data()
