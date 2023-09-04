class Checker:
    @staticmethod
    def if_not_str_raise_type_error(string):
        if string is not str:
            raise TypeError("Incompatible Typ!")

    @staticmethod
    def is_none_raise_type_error(param):
        if param is None:
            raise TypeError("Parameter was None!")

    @staticmethod
    def if_not_color_list_raise_type_error(param):
        if param is None:
            raise TypeError("Parameter is not a color-enum!")

    @staticmethod
    def if_not_dict_raise_type_error(string):
        if not isinstance(string,dict):
            raise TypeError("Incompatible Typ!")