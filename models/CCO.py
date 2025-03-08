import xmltodict
import json
class CCO:
    def __init__(self, file_xml):
        # Tree structure
        self.points = []
        self.lines = []

        try:
            # File location
            self.adr_xml = file_xml

            self.__read_file__()

            # Get pPerf n pTerm (Pascal)
            for attr in self.__tree_dict__["gxl"]["graph"]["info_graph"]["attr"]:
                    if attr["@name"].strip() == "pPerf":
                        self.pPerf = int(attr["float"])
                    if attr["@name"].strip() == "pTerm":
                        self.pTerm = int(attr["float"])

            self.__get_points__()
            self.__get_lines__()
            self.__calc_levels__()
        except:
            raise SyntaxError("ERROR: Something is wrong with the xml structure")

    # Convert XML to a dict
    def __read_file__(self):
        with open(self.adr_xml, "rb") as xml_file:
            self.__tree_dict__ = xmltodict.parse(xml_file) 

    # Get points of the tree
    def __get_points__(self):
        nodes = self.__tree_dict__.get("gxl", {}).get("graph", {}).get("node", [])
        
        for node in nodes:
            node_id = int(node["@id"].replace("n", ""))
            node_data = {
                "id": node_id,
                 "floats": []
            }

            for attr in node.get("attr", []):
                if "tup" in attr and "float" in attr["tup"]:
                    node_data["floats"].extend(map(float, attr["tup"]["float"]))

            self.points.append(node_data)
        


    # Get lines of the tree
    def __get_lines__(self):
        edges = self.__tree_dict__.get("gxl", {}).get("graph", {}).get("edge", [])
    
        for edge in edges:
            edge_data = {
                "from": int(edge["@from"].replace("n", "")),
                "to": int(edge["@to"].replace("n", "")),
                "radius": None,
                "resistance": None,
                "flow": None,
                "level": -1
            }
            
            for attr in edge.get("attr", []):
                if attr["@name"].strip() == "flow":
                    edge_data["flow"] = float(attr["float"])
                if attr["@name"].strip() == "resistance":
                    edge_data["resistance"] = float(attr["float"])
                if attr["@name"].strip() == "radius":
                    edge_data["radius"] = float(attr["float"])
            
            self.lines.append(edge_data)

    # Get levels of the tree
    def __calc_levels__(self):
        temp_lines = self.lines.copy()
        levels = [[]]
        
        self.lines[0]["level"] = 0
        temp_lines.pop(0)
        levels[0] = [self.lines[0]["to"]]
        
        while temp_lines:
            for line in temp_lines:
                from_node = line["from"]
                to_node = line["to"]
                
                for j, level in enumerate(levels):
                    if from_node in level:
                        if len(levels) <= j + 1:
                            levels.append([]) 
                        
                        self.lines[self.lines.index(line)]["level"] = j + 1
                        levels[j + 1].append(to_node)
                        temp_lines.remove(line) 
                        break

