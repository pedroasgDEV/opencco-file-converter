import xmltodict
import math
import numpy as np

class CCO:
    def __init__(self, file_xml):
        # Initialize tree structure
        self.points = []  # List to hold points data
        self.lines = []   # List to hold lines data
        self.volume = 0   # Total tree volume
        self.radius_level = [[]] #Get the segmente radius per birfubifurcation level

        self.adr_xml = file_xml # Store XML file location

        try:
            # Read and parse the XML file
            self.__read_file__()

            # Extract 'pPerf' and 'pTerm' values
            for attr in self.__tree_dict__["gxl"]["graph"]["info_graph"]["attr"]:
                if attr["@name"].strip() == "pPerf":
                    self.pPerf = int(attr["float"]) # Pa
                if attr["@name"].strip() == "pTerm":
                    self.pTerm = int(attr["float"]) # Pa

            # Get points, lines, and calculate levels
            self.__get_points__()
            self.__get_lines__()
            self.__calc_levels_pressure__()

        except:
            raise SyntaxError("ERROR: Something is wrong with the xml structure")

    # Convert XML file into a Python dictionary
    def __read_file__(self):
        with open(self.adr_xml, "rb") as xml_file:
            self.__tree_dict__ = xmltodict.parse(xml_file)

    # Extract points (nodes)
    def __get_points__(self):
        nodes = self.__tree_dict__.get("gxl", {}).get("graph", {}).get("node", [])

        if isinstance(nodes, dict):
            nodes = [nodes]
        
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

        if isinstance(edges, dict):
            edges = [edges]
    
        for edge in edges:
            edge_data = {
                "from": int(edge["@from"].replace("n", "")),  # Extract 'from' node
                "to": int(edge["@to"].replace("n", "")),      # Extract 'to' node
                "length": None, # mm
                "radius": None, # mm
                "volume": None, # mm³
                "resistance": None, # Pa·s/mm³
                "flow": None, # mm³/s
                "pPerf": None, # Pa
                "pTerm": None, # Pa
                "level": -1  # Initialize level for edge
            }

            # Extract edge attributes (flow, resistance, radius)
            for attr in edge.get("attr", []):
                if attr["@name"].strip() == "flow":
                    edge_data["flow"] = float(attr["float"]) / 60.0 #  µL/min -> mm³/s 
                if attr["@name"].strip() == "resistance": 
                    edge_data["resistance"] = float(attr["float"]) # Pa·s/mm³
                if attr["@name"].strip() == "radius":
                    edge_data["radius"] = float(attr["float"]) # mm
            
            # Get the coordinates of each point
            pFrom = self.points[edge_data["from"]]["floats"]
            pTo = self.points[edge_data["to"]]["floats"]

            # Calc Length
            edge_data["length"] = np.linalg.norm(np.array(pTo) - np.array(pFrom)) * 10 # mm

            # Calc Volume
            edge_data["volume"] = math.pi * (edge_data["radius"] ** 2) * edge_data["length"]
            self.volume += edge_data["volume"] # mm³

            self.lines.append(edge_data)

    # Calculate levels for nodes in the tree based ogitn their connections
    # Calculate perfusion n terminal pressure for each line
    def __calc_levels_pressure__(self):
        temp_lines = self.lines.copy()  # Make a copy of the lines
        levels = [[]]  # List to store levels of nodes
        levels_pressure = [[]]  # List to store terminal pressure of lines
        
        # Initialize the first line
        self.lines[0]["level"] = 0  # Assign level 0 to the first line
        self.lines[0]["pPerf"] = self.pPerf  # Assign model perfusion pressure in first line
        self.lines[0]["pTerm"] = self.lines[0]["pPerf"] - self.lines[0]["resistance"] * self.lines[0]["flow"]  # Calculate terminal pressure for the first line
        
        temp_lines.pop(0)  # Remove the first line from temp_lines
        levels[0] = [self.lines[0]["to"]]  # Initialize level 0 with the 'to' node of the first line
        levels_pressure[0] = [self.lines[0]["pTerm"]]  # Initialize level 0 with pTerm of the first line
        self.radius_level[0] = [self.lines[0]["radius"]] # Initialize level 0 with radius of the first line
        
        # Loop through remaining lines and assign levels based on connected nodes
        while temp_lines:
            for line in temp_lines:
                from_node = line["from"]
                to_node = line["to"]
                
                for j, level in enumerate(levels):
                    if from_node in level:
                        # If node is found in any level, assign next level
                        if len(levels) <= j + 1:
                            # Add a new level if needed
                            levels.append([])
                            levels_pressure.append([])
                            self.radius_level.append([])
                        
                        # Get the position of the line in self.lines
                        position_line = self.lines.index(line)  
                        # Get the position of the from_node in the level
                        position_pTerm = level.index(from_node)  

                        # Update the current line's level and pressures
                        self.lines[position_line]["level"] = j + 1
                        self.lines[position_line]["pPerf"] = levels_pressure[j][position_pTerm]  # pPerf is equal to the pTerm of the last segment
                        self.lines[position_line]["pTerm"] = self.lines[position_line]["pPerf"] - self.lines[position_line]["resistance"] * self.lines[position_line]["flow"]
                        
                        # Add the 'to' node and its corresponding pressure to the next level
                        levels[j + 1].append(to_node)  # Add 'to' node to the next level
                        levels_pressure[j + 1].append(self.lines[position_line]["pTerm"])  # Add pTerm of the line to the next level
                        self.radius_level[j + 1].append(self.lines[position_line]["radius"]) # Add radius of the line to the next level
                        temp_lines.remove(line)  # Remove processed line from temp_lines
                        break

