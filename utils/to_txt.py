from models.CCO import CCO

class TO_TXT:
    def __init__(self, cco: CCO, file_txt="output.txt"):
        self.__CCO__ = cco  # Store the CCO object
        self.adr_txt = file_txt  # Define output file path

        try:
            self.__write__()  # Write data to the file
        except:
            raise IOError("ERROR: Something went wrong while writing the txt file")

    # Write the CCO tree structure to a text file
    def __write__(self):
        with open(self.adr_txt, "w") as file:
            for line in self.__CCO__.lines:
                from_node = line["from"]
                to_node = line["to"]
                radius = f"{line['radius']:.6E}"  # Format radius in scientific notation
                level = line["level"]
                
                file.write(f"{from_node} {to_node} {radius} {level} #\n")  # Write data
