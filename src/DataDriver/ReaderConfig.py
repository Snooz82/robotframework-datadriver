class ReaderConfig:

    def __init__(self,
                 file=None,
                 encoding=None,
                 dialect=None,
                 delimiter=None,
                 quotechar=None,
                 escapechar=None,
                 doublequote=None,
                 skipinitialspace=None,
                 lineterminator=None,
                 sheet_name=None,
                 testcase_table_name=None
                 ):

        self.ROBOT_LIBRARY_LISTENER = self

        self.file = file
        self.encoding = encoding
        self.dialect = dialect
        self.delimiter = delimiter
        self.quotechar = quotechar
        self.escapechar = escapechar
        self.doublequote = doublequote
        self.skipinitialspace = skipinitialspace
        self.lineterminator = lineterminator
        self.sheet_name = sheet_name
        self.testcase_table_name = testcase_table_name
