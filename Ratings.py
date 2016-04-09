from FileCommonGetter import FilecommonGetter


class Ratings(FilecommonGetter):
    def __init__(self, src_path, dst_path):
        super(Ratings, self).__init__(src_path, dst_path)
        self.file_name = None
        self.user_id = []
        self.movie_id = []
        self.rating = []
        self.time_stamp = []

################# user api #####################################################
    def prepare_user_data(self, separator='::'):
        self.prepare()
        self.split_data_in_files(separator=separator)
        self.get_file_name('rating')
        self.split_list_to_separate_list()
        self.normalize_necessary_vectors()
        self.output = self.prepare_output_to_save_to_file(self.user_id, self.movie_id, self.rating, self.time_stamp)
        self.save_to_file(self.output, self.file_name)

############### private api #####################################################

    def split_list_to_separate_list(self):
        for index, line in enumerate(getattr(self, self.file_name)):
            self.user_id.append(line[0])
            self.movie_id.append(line[1])
            self.rating.append(line[2])
            self.time_stamp.append(line[3])

    def normalize_necessary_vectors(self):
        self.normalize_rating_vector()

    def normalize_rating_vector(self):
        self.rating = self.normalize_vector(self.rating, norm='max', max_value=5)

if __name__ == '__main__':
    ratings = Ratings("E:\Studia\ES\ml-1m", 'E:\Studia\ES\ml-1m\output')
    ratings.prepare_user_data()
