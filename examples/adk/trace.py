from westpa.analysis import Run
from westpa.analysis import HDF5MDTrajectory

run = Run.open("./west.h5")

#iteration = run.iteration(77)
iteration = run.iteration(64)

#walker = iteration.walker(94)
walker = iteration.walker(86)

trace = walker.trace()

trajectory = HDF5MDTrajectory()

traj = trajectory(trace)

traj.save("reppath2.dcd")
