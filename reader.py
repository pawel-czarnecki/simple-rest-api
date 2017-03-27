import yaml


class Reader:
    """Implementation of YML file reader"""

    def __init__(self, file_name='config.yml'):
        self.file_name = file_name

    def read_yml(self):
        """
        :return: Dictionary of all branches
        """
        if not isinstance(self.file_name, str):
            raise TypeError('File name must be a string')

        try:
            with open(self.file_name, 'r') as yml:
                try:
                    return yaml.load(yml)
                except yaml.YAMLError as e:
                    print(e)
        except FileNotFoundError as e:
            print(e)

        return {}

    def get_branch(self, branch='urls'):
        """
        :param branch: Name of the branch which we are looking for
        :return: List of dictionary located in the branch
        """
        for key, val in self.read_yml().items():
            if key == branch:
                return val

        return []
