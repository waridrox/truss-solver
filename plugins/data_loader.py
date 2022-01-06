# plugins/data_loader.py
import pandas as pd

class DataLoader:
    def __init__(self, elements_file, joints_file):
        self.elements_file = elements_file
        self.joints_file = joints_file

    def load_data(self):
        # Load the Excel files into pandas DataFrames.
        elements = pd.read_excel(self.elements_file, sheet_name="Element")
        joints = pd.read_excel(self.joints_file, sheet_name="Joint")
        # Optionally set the "Joint" column as the index for easier lookup.
        if "Joint" in joints.columns:
            joints.set_index("Joint", inplace=True)
        return elements, joints
