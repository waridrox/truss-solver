# plugins/plotter.py
import matplotlib.pyplot as plt
from statistics import mean

class Plotter:
    def __init__(self, elements, joints):
        self.elements = elements
        self.joints = joints

    def plot_truss(self):
        plt.figure(figsize=(8, 6))
        for i, name in enumerate(self.elements["Name"]):
            # Assuming each element name is a two-letter string, where each letter is a joint label.
            joint1 = name[0]
            joint2 = name[1]
            x_coord = [self.joints.loc[joint1]["X"], self.joints.loc[joint2]["X"]]
            y_coord = [self.joints.loc[joint1]["Y"], self.joints.loc[joint2]["Y"]]
            
            plt.plot(x_coord, y_coord, "ro-")
            plt.text(mean(x_coord), mean(y_coord), str(round(self.elements["Value"][i], 2)), fontsize=12)
            plt.text(x_coord[0], y_coord[0], joint1, fontsize=12, color="b", fontweight="bold")
            plt.text(x_coord[1], y_coord[1], joint2, fontsize=12, color="b", fontweight="bold")
            
        plt.title("Truss Structure with Forces")
        plt.xlabel("X Coordinate")
        plt.ylabel("Y Coordinate")
        plt.grid(True)
        plt.show()
