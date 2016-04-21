import os
import re

class FilecommonGetter(object):
    def __init__(self, src_path, dst_path, extension='dat'):
        self.src_path = src_path
        self.dst_path = dst_path
        self.file_names = []
        self._file_names_as_variables = []
        self.extension = extension

######### user api ####################################################################################################
    def prepare(self):
        self.get_file_names()
        self.set_file_names_as_variables()
        self.get_data_from_file()

    def prepare_output_to_save_to_file(self, *args, **kwargs):

        output_data = []
        for row_number in range(len(args[0])):
            tmp_list = ''
            for column_number in range(len(args)):
                tmp_list += "{};".format(args[column_number][row_number])
            if 'genres' in kwargs:
                for genres_types in kwargs['genres'][row_number]:
                    tmp_list += "{};".format(genres_types)
            output_data.append(tmp_list)
        return output_data

    def save_to_file(self, output, file_name):
        if not os.path.exists(self.dst_path):
            os.mkdir(self.dst_path)
        with open(os.path.join(os.sep, self.dst_path, '{}.csv'.format(file_name)), 'wb') as output_data_file:
            for line in output:
                output_data_file.write('{}\n'.format(line))


######### private api #################################################################################################
    def get_file_names(self):
        self.file_names = [file for file in next(os.walk(self.src_path))[2] if file.endswith('.dat')]

    def set_file_names_as_variables(self):
        self._file_names_as_variables = [file.split('.')[0] for file in self.file_names]

    def get_data_from_file(self):
        for file in self._file_names_as_variables:
            with open(os.path.join(os.sep, self.src_path, '{}.{}'.format(file, self.extension)), 'rb') as data_file:
                if file == 'ratings':
                    setattr(self, file, [line[:-1] for line in data_file])
                else:
                    setattr(self, file, [line[:-1] for line in data_file])

    def get_file_name(self, name):
        for key in self.__dict__.keys():
            match = re.match('(%s.*)' % name, key)
            if match:
                self.file_name = match.group()

    def normalize_vector(self, vector, norm='max', max_value=None):
        if norm == 'max':
            if max_value:
                return [float(element)/max_value for element in vector]
            else:
                return [float(element)/float(max(vector)) for element in vector]
        else:
            raise NotImplementedError

    def split_data_in_files(self, separator="::"):
        for file in self._file_names_as_variables:
            for index, line in enumerate(getattr(self, file)):
                getattr(self, file)[index] = line.split(separator)


if __name__ == '__main__':
    filecommongetter = FilecommonGetter("E:\Studia\ES\ml-1m", 'E:\Studia\ES\ml-1m\output')
    filecommongetter.prepare()
    filecommongetter.split_data_in_files()


