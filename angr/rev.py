# Import Angr
import angr
#import ply.yacc
#from .c_parser import CParser


# Establish the Angr Project
target = angr.Project('r100')

# Specify the desired address which means we have the correct input
desired_adr = 0x400849

# Specify the address which if it executes means we don't have the correct input
wrong_adr = 0x40085a

# Establish the entry state
entry_state = target.factory.entry_state(args=["./fairlight"])

# Establish the simulation
simulation = target.factory.simulation_manager(entry_state)

# Start the simulation
simulation.explore(find = desired_adr, avoid = wrong_adr)

solution = simulation.found[0].posix.dumps(0)
print(solution)
