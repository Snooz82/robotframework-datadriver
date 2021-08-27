from DataDriver import DataDriver
from inspect import getdoc

with open("Readme.rst", "w", encoding="utf-8") as readme:
    doc_string = getdoc(DataDriver)
    readme.write(str(doc_string).replace("\\", "\\\\").replace("\\\\*", "\\*"))
