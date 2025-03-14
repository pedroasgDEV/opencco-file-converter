import xmltodict
import math
import numpy as np

class CCO:
    def __init__(self, file_xml):
        # Initialize tree structure
        self.points = []  # List to hold points data
        self.lines = []   # List to hold lines data
        self.volume = 0   # Total tree volume

        self.adr_xml = file_xml # Store XML file location

        try:
            # Read and parse the XML file
            self.__read_file__()

            # Extract 'pPerf' and 'pTerm' values
            for attr in self.__tree_dict__["gxl"]["graph"]["info_graph"]["attr"]:
                if attr["@name"].strip() == "pPerf":
                    self.pPerf = int(attr["float"])
                if attr["@name"].strip() == "pTerm":
                    self.pTerm = int(attr["float"])

            # Get points, lines, and calculate levels
            self.__get_points__()
            self.__get_lines__()
            self.__calc_levels__()

        except:
            raise SyntaxError("ERROR: Something is wrong with the xml structure")

    # Convert XML file into a Python dictionary
    def __read_file__(self):
        with open(self.adr_xml, "rb") as xml_file:
            self.__tree_dict__ = xmltodict.parse(xml_file)

    # Extract points (nodes)
    def __get_points__(self):
        nodes = self.__tree_dict__.get("gxl", {}).get("graph", {}).get("node", [])
        
        for node in nodes:
            node_id = int(node["@id"].replace("n", ""))  # Extract node ID
            node_data = {
                "id": node_id,
                "floats": []  # List to hold float (x, y, z) values from node attributes
            }

            # Extract float (x, y, z) values from node attributes
            for attr in node.get("attr", []):
                if "tup" in attr and "float" in attr["tup"]:
                    node_data["floats"].extend(map(float, attr["tup"]["float"]))

            self.points.append(node_data)

    # Extract lines (edges) from the XML tree
    def __get_lines__(self):
        edges = self.__tree_dict__.get("gxl", {}).get("graph", {}).get("edge", [])
    
        for edge in edges:
            edge_data = {
                "from": int(edge["@from"].replace("n", "")),  # Extract 'from' node
                "to": int(edge["@to"].replace("n", "")),      # Extract 'to' node
                "length": None,
                "radius": None,
                "volume": None,
                "resistance": None,
                "flow": None,
                "level": -1  # Initialize level for edge
            }

            # Extract edge attributes (flow, resistance, radius)
            for attr in edge.get("attr", []):
                if attr["@name"].strip() == "flow":
                    edge_data["flow"] = float(attr["float"])
                if attr["@name"].strip() == "resistance":
                    edge_data["resistance"] = float(attr["float"])
                if attr["@name"].strip() == "radius":
                    edge_data["radius"] = float(attr["float"])
            
            # Get the coordinates of each point
            pFrom = self.points[edge_data["from"]]["floats"]
            pTo = self.points[edge_data["to"]]["floats"]

            # Calc Length
            edge_data["length"] = np.linalg.norm(np.array(pTo) - np.array(pFrom))

            # Calc Volume
            edge_data["volume"] = math.pi * (edge_data["radius"] ** 2) * edge_data["length"]
            self.volume += edge_data["volume"]

            self.lines.append(edge_data)

    # Calculate levels for nodes in the tree based ogitn their connections
    def __calc_levels__(self):
        temp_lines = self.lines.copy()  # Make a copy of the lines
        levels = [[]]  # List to store levels of nodes
        
        self.lines[0]["level"] = 0  # Assign level 0 to the first line
        temp_lines.pop(0)  # Remove the first line from temp_lines
        levels[0] = [self.lines[0]["to"]]  # Initialize level 0 with the 'to' node of the first line
        
        # Loop through remaining lines and assign levels based on connected nodes
        while temp_lines:
            for line in temp_lines:
                from_node = line["from"]
                to_node = line["to"]
                
                for j, level in enumerate(levels):
                    if from_node in level:
                        # If node is found in any level, assign next level
                        if len(levels) <= j + 1:
                            levels.append([])  # Add a new level if needed
                        
                        self.lines[self.lines.index(line)]["level"] = j + 1
                        levels[j + 1].append(to_node)  # Add 'to' node to the next level
                        temp_lines.remove(line)  # Remove processed line from temp_lines
                        break