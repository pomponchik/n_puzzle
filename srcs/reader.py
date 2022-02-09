from srcs.goodbye import goodbye


class Reader:
    def __init__(self, path):
        self.path = path
        self.strings = self.get_strings(self.path)
        if len(self.strings) < 4:
            goodbye('The file is too small.')

    def get_size_and_data_from_file(self):
        number_string = self.strings[0]
        other_strings = self.strings[1:]
        size = self.get_size_from_string(number_string)

        return size, self.get_data_from_strings(other_strings, size)

    def get_size_from_string(self, size_string):
        try:
            size = int(size_string)
            if size < 3:
                goodbye('You have specified a field size that is too small.')
            return size
        except:
            goodbye('Incorrect file format.')

    def get_data_from_strings(self, data_strings, size):
        if len(data_strings) != size:
            goodbye('The size of the field does not match the specified one.')

        result = []

        try:
            for string in data_strings:
                number_of_numbers = 0
                for number_substring in string.split():
                    number = int(number_substring)
                    if number < 0:
                        goodbye('The field can only contain numbers greater than zero.')
                    result.append(number)
                    number_of_numbers += 1
                if number_of_numbers != size:
                    goodbye('The size of the field does not match the specified one.')
        except:
            goodbye('Incorrect file format.')

        self.check_data(result)
        return result

    def check_data(self, numbers):
        if len(set(numbers)) != len(numbers):
            goodbye('Duplicate numbers on the field.')
        if max(numbers) != len(numbers) - 1:
            goodbye('Incorrect numbers on the field.')

    def get_strings(self, path):
        try:
            strings = []

            with open(path, 'r') as file:
                for string in file:
                    before_octothorpe = string.split('#')[0].strip()
                    if before_octothorpe:
                        strings.append(before_octothorpe)

            return strings
        except Exception as e:
            goodbye('The file or the path to it is invalid.')
