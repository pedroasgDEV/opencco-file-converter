from models.CCO import CCO

import json

class TO_JSON:
    def __init__(self, cco: CCO, file_json="output.json"):
        self.__CCO__ = cco  # Store the CCO object
        self.adr_json = file_json  # Define output file path

        try:
            self.__write__()  # Write data to the file
        except:
            raise IOError("ERROR: Something went wrong while writing the json file")

    # Write the model dict to a json file
    def __write__(self):
        cco_dict = self.__CCO__.__dict__
        cco_dict.pop("__tree_dict__", None) # Pop xml data from the dict
        with open(self.adr_json, 'w') as file:
            json.dump(cco_dict, file, indent=4)
