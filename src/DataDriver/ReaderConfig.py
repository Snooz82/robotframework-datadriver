class ReaderConfig:

    TEST_CASE_TABLE_NAME = '*** Test Cases ***'

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


class TestCaseData:

    def __init__(self,
                 test_case_name='',
                 arguments=None,
                 tags=None,
                 documentation=''
                 ):

        self.test_case_name = test_case_name
        self.arguments = arguments if arguments else {}
        self.tags = tags if tags else []
        self.documentation = documentation
