class DataFrameBuidlerException(Exception):
    pass


class EmptyColumnMappingException(DataFrameBuidlerException):
    pass


class InvalidFacebookColumnException(DataFrameBuidlerException):
    pass
