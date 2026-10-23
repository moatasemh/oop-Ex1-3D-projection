# 3D Volume Planar Projection (Ex1 — Intro to Software Engineering)

**Author:** Moatasem · **Course:** OOP/OOD · **Language:** Java

## Problem Definition
Given a 3D raster matrix M (NRRD, e.g., MRI) and a plane p defined by 3 or 4
co-planar points, compute a 2D matrix E — a dense rasterized sampling of p
within the volume. The problem is intentionally under-specified; a detailed
design is required (see SRS.md).

## Scope
- NRRD parsing + CSV point parsing + MP4 output.
- Core: plane rasterization / vector-stepping sampling (Sec. 5 of the spec).
- Performance: ≥30 FPS (must), 100+ FPS target, 500³ bytes input.
- Testing strategy + demo CLI.

## Repository Layout
- `src/` — implementation
- `docs/SRS.md` — Software Requirements Spec
- `docs/ALGORITHM.md` — detailed algorithm
- `data/` — NRRD dataset (source, size)
- `tests/` — unit + integration tests
- `out/` — sample MP4s

## Usage
python Ex0.py file.nrrd file.csv file.mp4

## Dataset
1. **MRHead.nrrd** (Real Data): Obtained from 3D Slicer sample data. Size: 256x256x130, Data Type: uint8. Used for the visual demo and functional testing.
2. **Synthetic_500.nrrd** (Benchmark Data): A generated 500x500x500 volume (Data Type: uint8). Because the MRHead file is too small to test the performance requirement, this file is used to prove the ≥30 FPS requirement on a 500^3 matrix.
3. **Planes.csv** (Coordinates): Contains test cases including 3-point planes (isosceles triangles) and 4-point planes (trapezoids).

## Testing
See `docs/SRS.md` Testing. Covers: degenerate planes, out-of-volume p,
EPS tolerance (0.001), 4-point trapezoid case, FPS benchmark.