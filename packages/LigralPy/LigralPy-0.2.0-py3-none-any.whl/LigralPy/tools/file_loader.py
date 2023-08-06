import os
from LigralPy.config import DEMOS_FOLDER


def load_demo(demo_name: str) -> str:
    """
    Load Demonstration
    """
    demo_file = os.path.join(DEMOS_FOLDER, demo_name) + ".json"
    with open(demo_file, "r") as f:
        return f.read()
