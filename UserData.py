from FileCommonGetter import FilecommonGetter
import re
import numpy as np

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
        self.unify_zip_codes()
        self.normalize_necessary_vectors()
        # self.output = self.prepare_output_to_save_to_file(self.user_id, self.gender, self.age, self.occupation, self.zip_code)
        # self.save_to_file(self.output, self.file_name)

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

    def unify_zip_codes(self):
        for index, zip_code in enumerate(self.zip_code):
            try:
                self.zip_code[index] = int(zip_code)
            except ValueError:
                self.zip_code[index] = int(zip_code.replace("-", ""))

    def create_friends(self):
        # zip_codes = []
        # for zip_code in self.zip_code:
        #     zip_codes.append(zip_code)
            # print zip_code
        # mean = sum(self.zip_code)/len(self.zip_code)
        # _min = min(self.zip_code)
        # _max = max(self.zip_code)
        # print _max - _min
        # print _max - mean
        # print len(self.zip_code)
        zip_zero = self.zip_code[0]
        seventy_percent = len(self.zip_code)*0.7
        print "70\% = ", seventy_percent
        # i=0
        k = []
        for zz in self.zip_code:
            # print self.zip_code.index(zz)
            for j in xrange(20000,121000,5000):
                i = 0
                for index,zip_code in enumerate(self.zip_code):
                    if abs(zip_code - zz) < j:
                        i += 1
                if i > seventy_percent:
                    # print "udalo sie!"
                    # print "i = ", i
                    # print "j = ", j
                    k.append(j)
                    break
            # else:
            #     print i
                # print "aktualnie j = ", j

        print len(k)
        print sum(k)/len(k)



if __name__ == '__main__':
    userdata = UserData("D:\PycharmProjects\SocialCommunicationNetworks\ml-1m", 'D:\PycharmProjects\SocialCommunicationNetworks\ml-1m\output')
    userdata.prepare_user_data()
    userdata.create_friends()