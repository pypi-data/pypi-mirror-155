import os
import json
from nodes import Node


def run(nodes):
    j_list = []
    for node in nodes:
        content: Node = node
        j_list.append(content.generate_ligjson())
    json1 = {"settings": [], "models": j_list}
    text = json.dumps(json1, indent=4)
    ligral_path = r"ligral.exe"
    file_path = os.path.join(os.path.dirname(__file__), "temp.lig.json")
    with open(file_path, "w") as f:
        f.write(text)
    os.popen("%s %s --json" % (ligral_path, file_path))
