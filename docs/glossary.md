# Glossary

Plain-language definitions for someone coming from medical (CCTA) segmentation. Where a
coronary analogue helps, it is given in brackets. Newest additions at the bottom of each
section.

## Rock and flow

- **Pore**: the empty space inside a rock (filled with water, oil or gas in the ground,
  air in a dry lab sample). In our masks pore = `True`. (Analogue: the vessel lumen.)
- **Grain**: the solid mineral, mostly quartz in sandstone. Mask value `False`.
  (Analogue: everything outside the lumen.)
- **Pore body**: a wide part of the pore space, roughly the gap between several grains.
  (Analogue: a vessel segment.)
- **Throat**: the narrow neck connecting two pore bodies. Throats are where most of the
  resistance to flow sits, so a throat that is too narrow or wrongly closed in a
  segmentation changes the flow a lot. (Analogue: a stenosis, or a branch point.)
- **Porosity (φ)**: fraction of the volume that is pore. Sandstones are typically 0.1 to
  0.3. *Connected porosity* counts only pore space connected to the sample faces;
  isolated pockets do not carry flow.
- **Permeability (k)**: how easily a fluid flows through the rock under a pressure
  difference, from Darcy's law q = −(k/μ) ∇p, where q is the flow rate per unit area and
  μ the fluid viscosity. Units are area (m²); geologists use the **darcy** (D):
  1 D ≈ 9.87 × 10⁻¹³ m², and 1 millidarcy (mD) = 10⁻³ D. Sandstones span roughly
  1 mD to a few darcy. Permeability scales roughly with the square of the throat size,
  which is why throat errors matter. (Analogue: FFR is the flow quantity in CCTA;
  permeability plays that role here.)
- **Darcy velocity / superficial velocity**: flow rate divided by the whole
  cross-section (pore plus grain), not just the pore area.
- **Pore network model (PNM)**: the pore space reduced to a graph, pore bodies as nodes
  and throats as edges, each edge given a hydraulic conductance from its size. Solving
  flow on the graph is fast but approximate. (Analogue: a vessel centreline graph with
  radii.)
- **SNOW / SNOW2**: the standard algorithm (PoreSpy) that extracts a pore network from a
  segmented image by watershed segmentation of the distance map.
- **Percolation threshold**: the porosity below which the pore space no longer forms a
  connected path across the sample, so permeability drops to zero. Near this threshold a
  few throats carry all the flow, so single broken connections should matter most.
- **Representative elementary volume (REV)**: the smallest sample size for which a
  property (porosity, permeability) stops changing much as the sample grows. Below the
  REV, results depend on where you crop.
- **Formation factor**: ratio of the electrical resistivity of the brine-saturated rock to
  that of the brine alone; a second transport property that depends on connectivity.
- **Tortuosity**: how much longer the actual flow paths are than the straight distance
  through the sample.
- **Sub-resolution porosity**: pores smaller than one voxel; they appear as grey,
  partly-dark voxels and cannot be labelled cleanly. A big issue in carbonates
  (limestones), less so in clean sandstones.
- **Sandstone / carbonate**: sandstone is cemented sand grains (mostly quartz), with
  fairly simple pore space; carbonates (limestone, dolomite) have pores over many size
  scales and are harder to segment.
- **Berea, Bentheimer, Fontainebleau**: standard, widely-studied sandstones used as
  benchmarks.
- **Micro-CT**: X-ray computed tomography at micrometre voxel sizes. Pores look dark
  (low attenuation), grains look bright.
- **Lab permeability**: measured by pushing gas or liquid through a physical core plug
  (centimetres across). Image-based permeability is computed on a much smaller
  sub-volume (millimetres), so the two need not agree exactly.

## Topology and metrics

- **Connectivity (6 vs 26)**: in 3D a voxel has 6 face neighbours, 18 face-or-edge and
  26 face-edge-or-corner neighbours. We treat pore voxels as connected only through faces
  (6), because fluid cannot pass through an edge or a corner. Grain then uses 26, the
  matching "dual" choice, so the topology is consistent.
- **Betti numbers**: counts of topological features of the pore space. β0 = number of
  separate pore clusters; β1 = number of independent loops (ways to go round and come
  back: a donut has one); β2 = number of enclosed cavities (grains floating inside pore,
  rare). Pore networks have very large β1 because they are full of loops, unlike a
  coronary tree, which has β1 ≈ 0.
- **Euler number (Euler characteristic, χ)**: χ = β0 − β1 + β2. Strongly negative in
  well-connected rock (many loops). Usually reported per unit volume ("Euler density",
  per mm³) so different sample sizes can be compared. It is one of the four **Minkowski
  functionals** (volume, surface area, integrated mean curvature, Euler number), the
  standard set of shape descriptors in rock physics.
- **Dice / IoU**: voxel overlap scores, as in medical imaging.
- **clDice**: the harmonic mean of "topology precision" (the fraction of the predicted
  skeleton lying inside the reference) and "topology sensitivity" (the fraction of the
  reference skeleton inside the prediction). Designed for tubular structures; sensitive
  to breaks that hardly change Dice. *soft-clDice* is its differentiable loss version.
- **Skeleton Recall**: a cheaper topology-aware loss that rewards recovering a thickened
  ("tubed") skeleton of the reference.
- **Throat-level error (this project)**: throats of the reference and the predicted pore
  networks are paired one-to-one by position; unpaired reference throats are *missed*,
  unpaired predicted throats are *false*, and paired throats are compared by radius.
  This is our analogue of bifurcation-level scoring in coronary CT.

## Solvers

- **Lattice-Boltzmann method (LBM)**: a voxel-level flow solver. Instead of solving the
  Navier-Stokes equations directly, it tracks the probability of fluid "particles" moving
  along a fixed set of directions on the voxel grid (here 19 directions, called D3Q19)
  and relaxes them toward equilibrium at each step. Works directly on segmented images,
  no meshing needed.
- **TRT (two-relaxation-time)**: an LBM variant with two relaxation rates. With a
  particular ratio between them (the "magic" value Λ = 3/16) the computed permeability no
  longer depends on the chosen viscosity and the wall sits exactly halfway between pore
  and grain voxels.
- **Bounce-back**: the LBM wall rule: a particle hitting grain reverses direction, which
  gives zero velocity at the wall (no-slip).
- **Stokes flow**: slow, viscous flow where inertia is negligible; the right regime for
  permeability. Our solver drops the inertial term, so it solves Stokes flow exactly.
- **Grid refinement study**: rerunning the same geometry on a finer lattice to estimate
  how much the answer depends on the grid; that change is the solver's numerical error.
