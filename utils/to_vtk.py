from models.CCO import CCO

class TO_VTK:
    def __init__(self, cco: CCO, file_vtk="output.vtk"):
        self.__CCO__ = cco  # Store the CCO object
        self.adr_vtk = file_vtk  # Define output file path

        try:
            self.__write__()  # Write data to the VTK file
        except:
            raise IOError("ERROR: Something went wrong while writing the vtk file")

    # Write the CCO tree structure to a VTK file
    def __write__(self):
        with open(self.adr_vtk, "w") as file:
            file.write("# vtk DataFile Version 3.0\nvtk output\nASCII\nDATASET POLYDATA\n")
            self.__points__(file)
            self.__lines__(file)
            self.__flow__(file)
            self.__resistance__(file)
            self.__radius__(file)
            self.__length__(file)

    # Write point data to the VTK file
    def __points__(self, file):
        file.write(f"POINTS {len(self.__CCO__.points)} float\n")
        
        for point in self.__CCO__.points:
            if len(point['floats']) == 2:  # If only 2D coordinates are provided, assume z = 0
                file.write(f"{point['floats'][0]:.7f} {point['floats'][1]:.7f} {0:.7f}\n")
            else:
                file.write(f"{point['floats'][0]:.7f} {point['floats'][1]:.7f} {point['floats'][2]:.7f}\n")

    # Write connectivity (lines) between points
    def __lines__(self, file):
        file.write(f"\nLINES {len(self.__CCO__.lines)} {len(self.__CCO__.lines) * 3}\n")

        for line in self.__CCO__.lines:
            file.write(f"2 {line['from']} {line['to']}\n")  # '2' indicates a line with two points

        file.write(f"\nCELL_DATA {len(self.__CCO__.lines)}\n")


    # Write flow data as cell attributes
    def __flow__(self, file):
        file.write("scalars flow float\nLOOKUP_TABLE default\n")

        for line in self.__CCO__.lines:
            file.write(f"{line['flow']}\n")

    # Write resistance data as cell attributes
    def __resistance__(self, file):
        file.write("scalars resistance_relative_sub float\nLOOKUP_TABLE default\n")

        for line in self.__CCO__.lines:
            file.write(f"{line['resistance_relative_sub']:.7f}\n")

    # Write radius data as cell attributes
    def __radius__(self, file):
        file.write("scalars radius float\nLOOKUP_TABLE default\n")

        for line in self.__CCO__.lines:
            file.write(f"{line['radius']:.7f}\n")

    # Write length data as cell attributes
    def __length__(self, file):
        file.write("scalars length float\nLOOKUP_TABLE default\n")

        for line in self.__CCO__.lines:
            file.write(f"{line['length']:.7f}\n")