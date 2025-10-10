# Demonstrate the profiling of a trivial function:
import cProfile, time
def rest():
    time.sleep(2)

cProfile.run ( 'rest()' )