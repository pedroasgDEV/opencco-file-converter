from app.models.CCO import CCO

class TO_TXT:
    def __init__(self, cco : CCO, file_txt = "output.txt"):
        self.__CCO__ = cco
        self.adr_txt = file_txt

        try:
            self.__write__()
        except:
            raise IOError("ERROR: Something went wrong while writing the txt file")

    # Write cco tree in a txt
    def __write__(self):
        with open(self.adr_txt, "w") as file:
            for line in self.__CCO__.lines:
                from_node = line["from"]
                to_node = line["to"]
                radius = f"{line['radius']:.6E}" 
                level = line["level"]
                
                file.write(f"{from_node} {to_node} {radius} {level} #\n")