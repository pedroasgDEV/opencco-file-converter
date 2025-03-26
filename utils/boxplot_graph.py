from models.CCO import CCO

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import numpy as np

class BoxplotGraph:
    def __init__(self, cco: CCO, file_png="output.png"):
        self.__CCO__ = cco  # Store the CCO object
        self.adr_png = file_png  # Define output file path

        try:
            self.__write__()  # Write data to the file
        except:
            raise IOError("ERROR: Something went wrong while writing the png file")

    # Write the boxplot graph to a png file
    def __write__(self):
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=self.__CCO__.radius_level)
        plt.xticks(ticks=np.arange(len(self.__CCO__.radius_level)), labels=[f"Level {i}" for i in range(len(self.__CCO__.radius_level))])
        plt.xlabel("Birfucation level")
        plt.ylabel("Radius")
        plt.title("Distribution of Radius by Bifurcation Level")
        plt.grid(True, linestyle='--', alpha=0.6)
        
        plt.savefig(self.adr_png, dpi=300, bbox_inches='tight')
        plt.close()
