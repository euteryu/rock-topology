"""rocktopo: segmentation metrics scored by permeability in digital rock.

Convention used everywhere in this package: a binary mask is a 3D numpy bool array
indexed (z, y, x) with True = pore (void space) and False = grain (solid mineral).
Voxel sizes are in metres unless a name says otherwise.
"""

__version__ = "0.1.0"
