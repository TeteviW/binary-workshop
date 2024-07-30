# Import Angr
import angr
import claripy
#import code

# Establish the Angr Project
target = angr.Project('crackme', main_opts = {'base_addr': 0x0})

# Specify the desired address which means we have the correct input
desired_adr = 0x1220


# Specify the address which if it executes means we don't have the correct input
wrong_adr = 0x122e

# Flag is 10 characters
flag = claripy.BVS("flag", 8 * 10)

# Establish the entry state
entry_state = target.factory.entry_state(stdin = flag)

# Silence the warnings
entry_state.options.add(angr.options.ZERO_FILL_UNCONSTRAINED_MEMORY)

# Flags consists only on numbers ('0' -> '9')
for i in range(10):
    entry_state.solver.add(flag.get_byte(i) >= 48)
    entry_state.solver.add(flag.get_byte(i) <= 57)

# Establish the simulation
simulation = target.factory.simulation_manager(entry_state)

# Start the simulation
simulation.explore(find = desired_adr, avoid = wrong_adr)

#code.interact(local=locals())

solution = simulation.found[0].posix.dumps(0)

print(solution)
