from app.models.CCO import CCO

class TO_VTK:
    def __init__(self, cco: CCO, file_vtk="output.vtk"):
        self.__CCO__ = cco
        self.adr_vtk = file_vtk

        self.__write__()

    # Write cco tree in a txt
    def __write__(self):
        with open(self.adr_vtk, "w") as file:
            file.write("# vtk DataFile Version 3.0\nvtk output\nASCII\nDATASET POLYDATA\n")
            self.__points__(file)
            self.__lines__(file)
            self.__flow__(file)
            self.__resistance__(file)
            self.__radius__(file)

    def __points__(self, file):
        file.write(f"POINTS {len(self.__CCO__.points)} float\n")
        
        for point in self.__CCO__.points:
            if len(point['floats']) == 2:
                file.write(f"{point['floats'][0]:.7f} {point['floats'][1]:.7f} {0:.7f}\n")
            else:
                file.write(f"{point['floats'][0]:.7f} {point['floats'][1]:.7f} {point['floats'][2]:.7f}\n")

    def __lines__(self, file):
        file.write(f"\nLINES {len(self.__CCO__.lines)} {len(self.__CCO__.lines) * 3}\n")

        for line in self.__CCO__.lines:
            file.write(f"2 {line['from']} {line['to']}\n")

    def __flow__(self, file):
        file.write(f"\nCELL_DATA {len(self.__CCO__.lines)}\n")
        file.write("scalars flow float\nLOOKUP_TABLE default\n")

        for line in self.__CCO__.lines:
            file.write(f"{line['flow']}\n")

    def __resistance__(self, file):
        file.write("scalars resistance float\nLOOKUP_TABLE default\n")

        for line in self.__CCO__.lines:
            file.write(f"{line['resistance']:.7f}\n")

    def __radius__(self, file):
        file.write("scalars radius float\nLOOKUP_TABLE default\n")

        for line in self.__CCO__.lines:
            file.write(f"{line['radius']:.7f}\n")