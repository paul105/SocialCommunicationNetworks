from FileCommonGetter import FilecommonGetter
import re


class UserData(FilecommonGetter):
    def __init__(self, src_path, dst_path):
        super(UserData, self).__init__(src_path, dst_path)
        self.file_name = None
        self.user_id = []
        self.gender = []
        self.age = []
        self.occupation = []
        self.zip_code = []

################# user api #####################################################
    def prepare_user_data(self, separator='::'):
        self.prepare()
        self.split_data_in_files(separator=separator)
        self.get_file_name('user')
        self.split_list_to_separate_list()
        self.change_letter_to_number_in_sex_field()
        self.normalize_necessary_vectors()
        self.output = self.prepare_output_to_save_to_file(self.user_id, self.gender, self.age, self.occupation, self.zip_code)
        self.save_to_file(self.output, self.file_name)

############### private api #####################################################

    def split_list_to_separate_list(self):
        for index, line in enumerate(getattr(self, self.file_name)):
            self.user_id.append(line[0])
            self.gender.append(line[1])
            self.age.append(int(line[2]))
            self.occupation.append(int(line[3]))
            self.zip_code.append(line[4])

    def change_letter_to_number_in_sex_field(self):
        for index, element in enumerate(self.gender):
            if element == 'M':
                self.gender[index] = 0
            elif element == 'F':
                self.gender[index] = 1

    def normalize_age_vector(self):
        self.age = self.normalize_vector(self.age, norm='max')

    def normalize_occupation_vector(self):
        self.occupation = self.normalize_vector(self.occupation, norm='max')

    def normalize_necessary_vectors(self):
        self.normalize_age_vector()
        self.normalize_occupation_vector()


if __name__ == '__main__':
    userdata = UserData("E:\Studia\ES\ml-1m", 'E:\Studia\ES\ml-1m\output')
    userdata.prepare_user_data()
