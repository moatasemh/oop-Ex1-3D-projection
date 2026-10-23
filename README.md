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
NRRD files from 3D Slicer sample data (list + sizes).

## Testing
See `docs/SRS.md` Testing. Covers: degenerate planes, out-of-volume p,
EPS tolerance (0.001), 4-point trapezoid case, FPS benchmark.