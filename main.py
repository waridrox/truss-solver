# main.py
from plugins.data_loader import DataLoader
from plugins.reaction_solver import ReactionSolver
from plugins.element_solver import ElementSolver
from plugins.plotter import Plotter

def main():
    # Load the data from Excel files
    data_loader = DataLoader("data/Ex1.xlsx", "data/Ex1.xlsx") # extract elements & joints from excel sheets
    elements, joints = data_loader.load_data()
    
    # Solve reaction forces at joints
    reaction_solver = ReactionSolver(joints)
    joints = reaction_solver.solve_reactions()
    
    # Solve for forces in truss elements
    element_solver = ElementSolver(elements, joints)
    elements, joints = element_solver.solve_elements()
    
    # Plot the truss with calculated forces
    plotter = Plotter(elements, joints)
    plotter.plot_truss()

if __name__ == '__main__':
    main()
