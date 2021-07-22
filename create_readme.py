from DataDriver import DataDriver

def main():
    with open("Readme.rst", "w", encoding="utf-8") as readme:
        doc_string = DataDriver.__doc__
        readme.write(str(doc_string).replace("\\", "\\\\").replace("\\\\*", "\\*"))

if __name__ == "__main__":
    main()