
class Config(object):

    def __init__(self, data: dict):
        super(Config, self).__init__()
        self.__data = data

    def get(self, key, default=None):
        k_seq = self.__split_key(key)
        return self.__get_from_dict(self.__data, k_seq, default)

    def set(self, key, value):
        k_seq = self.__split_key(key)
        self.__set_to_dict(self.__data, k_seq, value)

    def remove(self, key):
        k_seq = self.__split_key(key)
        self.__remove_from_dict(self.__data, k_seq)

    @classmethod
    def __split_key(cls, key: str):
        if key is None or key.strip() == "":
            raise ValueError("key cannot be none or empty.")
        return key.split(".")

    @classmethod
    def __exists_in_dict(cls, d: dict, k_seq: list):
        if k_seq is None or len(k_seq) == 0:
            return False
        for k in k_seq:
            if k in d:
                d = d[k]
            else:
                return False
        return True

    @classmethod
    def __get_from_dict(cls, d: dict, k_seq: list, default=None):
        if k_seq is None or len(k_seq) == 0:
            raise ValueError("key cannot be none or empty")
        for k in k_seq:
            if k in d:
                d = d[k]
            else:
                return False, default
        return True, d

    @classmethod
    def __remove_from_dict(cls, d: dict, k_seq: list):
        if k_seq is None or len(k_seq) == 0:
            raise ValueError("key cannot be none or empty")
        for k in k_seq[:-1]:
            if k not in d:
                return False
            d = d[k]
        try:
            del d[k_seq[-1]]
            return True
        except:
            return False

    @classmethod
    def __set_to_dict(cls, d: dict, k_seq: list, value):
        if k_seq is None or len(k_seq) == 0:
            raise ValueError("key cannot be none or empty")
        for k in k_seq[:-1]:
            if k not in d:
                d[k] = {}
            d = d[k]
        d[k_seq[-1]] = value
