from FileCommonGetter import FilecommonGetter
import re
import os
import random

class UserData(FilecommonGetter):
    def __init__(self, src_path, dst_path):
        super(UserData, self).__init__(src_path, dst_path)
        self.file_name = None
        self.user_id = []
        self.gender = []
        self.age = []
        self.occupation = []
        self.zip_code = []
        self.friends = {}

################# user api #####################################################
    def prepare_user_data(self, separator='::'):
        self.prepare()
        self.split_data_in_files(separator=separator)
        self.get_file_name('user')
        self.split_list_to_separate_list()
        self.change_letter_to_number_in_sex_field()
        self.unify_zip_codes()
        self.normalize_necessary_vectors()
        self.calculate_70per_cent_proximity()
        self.output = self.prepare_output_to_save_to_file(self.user_id, self.gender, self.age, self.occupation,
                                                          self.zip_code, friends=self.friends)
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

    def unify_zip_codes(self):
        for index, zip_code in enumerate(self.zip_code):
            zip_code = zip_code.replace('-', '')
            try:
                self.zip_code[index] = int(zip_code[:6])
            except ValueError:
                self.zip_code[index] = int(zip_code)
            self.friends[self.user_id[index]] = []


    def _create_friends_list(self, seventy_per_cent, index):
        people_farway = []
        people_nearby = []
        try:
            for u_index, _zip_code in enumerate(self.zip_code):
                if index == u_index:
                    continue
                if abs(_zip_code-self.zip_code[index]) < seventy_per_cent:
                    people_nearby.append(self.user_id[u_index])
                else:
                    people_farway.append(self.user_id[u_index])
            friends = random.sample(people_nearby, 35) + random.sample(people_farway, 15)
        except ValueError as err:
            raise ValueError("Cos poszlo nie tak, nie mam znajomych? :( {}, {}, {} \n {}".format(index,
                                                                                                 self.zip_code[index],
                                                                                                 seventy_per_cent, err))
        for friend in friends:
            if len(self.friends[friend]) < 50 \
                    and self.user_id[index] not in self.friends[friend] \
                    and len(self.friends[self.user_id[index]]) < 50:
                self.friends[self.user_id[index]].append(friend)
                self.friends[friend].append(self.user_id[index])

    def calculate_70per_cent_proximity(self):
        seventy_percent = len(self.zip_code)*0.7
        diffs = []
        for index1, zz in enumerate(self.zip_code):
            for j in xrange(30000, 9900000, 3000):
                i = 0
                for index,zip_code in enumerate(self.zip_code):
                    if abs(zip_code - zz) < j:
                        i += 1
                if i > seventy_percent:
                    diffs.append(j)
                    break
        if len(diffs) != 6040:
            raise Exception("Nie okreslono roznicy zip-code dla kogos. k = {}".format(len(diffs)))
        for index, zz in enumerate(self.zip_code):
            self._create_friends_list(diffs[index], index)



if __name__ == '__main__':
    root_path = 'C:\Users\p\Documents'
    input_files_path = os.path.join(root_path, 'PycharmProjects\SocialCommunicationNetworks\ml-1m')
    output_files_path = os.path.join(root_path, 'PycharmProjects\SocialCommunicationNetworks\ml-1m\output')
    userdata = UserData(input_files_path, output_files_path)
    userdata.prepare_user_data()
    userdata.calculate_70per_cent_proximity()
    k=0
    for friend in userdata.friends.keys():
        k += len(set(userdata.friends[friend]))
        print len(set(userdata.friends[friend]))
    print k
    print len(userdata.friends)
    print k/6040.0