#!/usr/bin/env python3
import argparse
from os import _exit


class YamlSplitter:
    """
    Class object for yaml splitter
    """

    def __init__(self, cwd="./", split=3):
        self.cwd = cwd
        self.split = split

    def load(self, filename):
        """
        Read .yaml file then return data as a list
        filename (str): .yaml filename
        """

        if self.cwd[-1] != "/" and self.cwd[-1] != "\\":
            self.cwd += "/"

        with open(f"{self.cwd}{filename}", "r", encoding="utf-8") as file:
            print(f"Loaded {self.cwd}{filename}\n")
            return [_.strip() for _ in file.readlines()]

    def write(self, cursor, data):
        """
        Writes given list of data to file
        cursor (str / int):  Part of filename
        data (list): List of strings to concat then write to file
        """
        filepath = f"{self.cwd}treatment_{self.split}_{cursor}.yaml"

        try:
            with open(filepath, "a", encoding="utf-8") as file: # Open file dynamically
                file.writelines("\n".join(data)) # Join list with newlines then write to file
                file.writelines("\n") # Write extra newline for readability
            print(f"Wrote {len(data)} lines to {filepath}")
        except PermissionError:
            print(f"No write permissions in {self.cwd}")
            _exit(0)

    def parse(self, data):
        """
        Parses .yaml file data

        Variables:
        data (str): yaml file data
        """

        cursor = 1

        # # Build list of strings
        tmp = []
        for line in data:
            tmp.append(line)
            if line == "": # If newline / blank string detected
                self.write(cursor, tmp)
                cursor += 1
                if cursor > self.split:
                    cursor = 1 # Reset cursor if its more than the allowed count
                tmp.clear() # Clear list of strings on write to file

        if len(tmp) > 0: # If newline missing at end of treatment.yaml
            self.write(cursor, tmp)

        print("Done!")
def main():
    """
    Main function handler
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--filepath", "-f", help="Location of treatment.yaml")
    args = parser.parse_args()

    if args.filepath:
        splitter = YamlSplitter(args.filepath)
    else:
        splitter = YamlSplitter()

    data = splitter.load("treatment.yaml")
    splitter.parse(data)

if __name__ == "__main__":
    main()


# Could maybe do with implementing something that
# Divides the last tunnel up assuming the last line does not end
# on the last robot
# i.e. if you select 3 robots, then the last line should fall on robot 3
# if not, then it should be divided between 2 and 3