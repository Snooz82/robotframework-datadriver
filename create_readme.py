from inspect import getdoc
from pathlib import Path

from DataDriver import DataDriver

with Path("Readme.rst").open("w", encoding="utf-8") as readme:
    doc_string = getdoc(DataDriver)
    readme.write(str(doc_string).replace("\\", "\\\\").replace("\\\\*", "\\*"))
