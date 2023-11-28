# pygameGravityEngine
Physics Engine built to model the gravitational forces between bodies. Built in pygame. The user clicks to add a body and the bodies move according to the laws of gravity.

The program has no particular optimisations and as a result has O(N^2). (Each body calculates the forces acting upon it and we do this for each body). This means that the program struggles to run for a high number of bodies. A quad tree or other such optimisations could be used to minimise this inefficiency.
