from DataDriver.AbstractReaderClass import AbstractReaderClass
from DataDriver.ReaderConfig import TestCaseData


class foo_reader(AbstractReaderClass):
    def get_data_from_source(self):
        return self._read_file_to_data_table()

    def _read_file_to_data_table(self):
        test_data = []
        flipflop = True
        for i in range(6):
            args = {"${fooarg}": i}
            tags = ["included"]
            if flipflop:
                tags = ["filtered"]
                flipflop = False
            else:
                flipflop = True
            if i == 3:
                tags = []
            test_data.append(TestCaseData(f"Test {i}", args, tags))
        return test_data
