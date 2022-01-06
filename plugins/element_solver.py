# plugins/element_solver.py
import numpy as np
import math
from collections import Counter
import operator
from statistics import mean

class ElementSolver:
    def __init__(self, elements, joints):
        self.elements = elements
        self.joints = joints

    def solve_elements(self):
        # Generate a two-letter name for each element from its start and end joints.
        self.elements["Name"] = [a + b for a, b in zip(self.elements["Start"], self.elements["End"])]
        self.elements["Value"] = [None] * len(self.elements)
        
        # Count the occurrence of each joint in the elements.
        letters = Counter(self.elements["Start"].tolist() + self.elements["End"].tolist())
        sorted_letters = sorted(letters.items(), key=operator.itemgetter(1))
        sorted_letters = [list(ele) for ele in sorted_letters]
        
        # Solve until all element forces have been computed.
        while None in self.elements["Value"].tolist():
            # Pick the joint with the fewest unknown connected elements.
            joint = sorted_letters[0][0]
            e_forces = []
            # Find connected elements that have not yet been solved.
            for i in range(len(self.elements)):
                if (joint in self.elements["Name"][i]) and (self.elements["Value"][i] is None):
                    e_forces.append(self.elements["Name"][i])
                    
            if len(e_forces) == 2:
                # When two unknown element forces are connected to the joint.
                angles = []
                for point in e_forces:
                    other_joint = point.replace(joint, "")
                    y_diff = self.joints.loc[other_joint]["Y"] - self.joints.loc[joint]["Y"]
                    x_diff = self.joints.loc[other_joint]["X"] - self.joints.loc[joint]["X"]
                    
                    if x_diff < 0:
                        angle = math.atan(y_diff / x_diff) + math.pi
                    elif x_diff > 0:
                        angle = math.atan(y_diff / x_diff)
                    else:
                        angle = math.pi / 2 if y_diff > 0 else -math.pi / 2
                    angles.append(angle)
                    
                    # Reduce the count of unknowns for the other joint.
                    for i in range(len(sorted_letters)):
                        if other_joint == sorted_letters[i][0]:
                            sorted_letters[i][1] -= 1
                
                # Set up equilibrium equations in x and y.
                left_x = [math.cos(angles[0]), math.cos(angles[1])]
                left_y = [math.sin(angles[0]), math.sin(angles[1])]
                right_x = -(self.joints.loc[joint]["RX"] + self.joints.loc[joint]["FX"])
                right_y = -(self.joints.loc[joint]["RY"] + self.joints.loc[joint]["FY"])
                
                a_matrix = np.array([left_x, left_y])
                b_vector = np.array([right_x, right_y])
                R = np.linalg.solve(a_matrix, b_vector).tolist()
                
                # Assign the computed forces to the corresponding elements.
                for idx, point in enumerate(e_forces):
                    self.elements.loc[self.elements["Name"] == point, "Value"] = round(R[idx], 2)
            else:
                # When there is only one unknown element connected to the joint.
                angles = []
                other_joint = e_forces[0].replace(joint, "")
                y_diff = self.joints.loc[other_joint]["Y"] - self.joints.loc[joint]["Y"]
                x_diff = self.joints.loc[other_joint]["X"] - self.joints.loc[joint]["X"]
                
                if x_diff < 0:
                    angle = math.atan(y_diff / x_diff) + math.pi
                elif x_diff > 0:
                    angle = math.atan(y_diff / x_diff)
                else:
                    angle = math.pi / 2 if y_diff > 0 else -math.pi / 2
                angles.append(angle)
                
                for i in range(len(sorted_letters)):
                    if other_joint == sorted_letters[i][0]:
                        sorted_letters[i][1] -= 1
                
                if angles[0] == 0:
                    a_matrix = np.array([[math.cos(angles[0])]])
                    b_vector = np.array([-(self.joints.loc[joint]["RX"] + self.joints.loc[joint]["FX"])])
                    result = np.linalg.solve(a_matrix, b_vector)[0]
                else:
                    a_matrix = np.array([[math.sin(angles[0])]])
                    b_vector = np.array([-(self.joints.loc[joint]["RY"] + self.joints.loc[joint]["FY"])])
                    result = np.linalg.solve(a_matrix, b_vector)[0]
                    
                self.elements.loc[self.elements["Name"] == e_forces[0], "Value"] = round(result, 2)
            
            # Update the forces at joints based on the solved element force(s).
            FX_forces = self.joints["FX"].tolist()
            FY_forces = self.joints["FY"].tolist()
            if len(e_forces) == 2:
                for idx, point in enumerate(e_forces):
                    other_joint = point.replace(joint, "")
                    angle = math.atan2(self.joints.loc[other_joint]["Y"] - self.joints.loc[joint]["Y"],
                                        self.joints.loc[other_joint]["X"] - self.joints.loc[joint]["X"])
                    for k, ind in enumerate(self.joints.index):
                        if other_joint == ind:
                            force = R[idx]
                            FX_forces[k] = FX_forces[k] - (force * math.cos(angle))
                            FY_forces[k] = FY_forces[k] - (force * math.sin(angle))
            else:
                other_joint = e_forces[0].replace(joint, "")
                angle = math.atan2(self.joints.loc[other_joint]["Y"] - self.joints.loc[joint]["Y"],
                                    self.joints.loc[other_joint]["X"] - self.joints.loc[joint]["X"])
                for k, ind in enumerate(self.joints.index):
                    if other_joint == ind:
                        force = result
                        FX_forces[k] = FX_forces[k] - (force * math.cos(angle))
                        FY_forces[k] = FY_forces[k] - (force * math.sin(angle))
                        
            self.joints["FX"] = FX_forces
            self.joints["FY"] = FY_forces
            
            # Remove the solved joint from the list and re-sort.
            sorted_letters.pop(0)
            sorted_letters = sorted(sorted_letters, key=operator.itemgetter(1))
        
        return self.elements, self.joints
