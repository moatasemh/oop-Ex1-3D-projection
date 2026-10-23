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

## Testing Strategy
Our testing strategy is divided into three main phases to ensure correctness, stability, and adherence to the demo requirements:

1. **Unit & Algorithm Testing:**
    - **Geometric Validation:** Testing the EPS (0.001) tolerance logic for both 3-point (isosceles triangle) and 4-point (trapezoid) planes.
    - **Edge Cases:** Verifying that degenerate planes (distance = 0) are handled without crashing, and that sampled points outside the 3D matrix boundaries strictly return `0`.
    - **Parsing:** Testing the NRRD reader and CSV reader with valid and malformed files.

2. **Integration & Output Testing:**
    - Validating the generated 2D matrix (E) dimensions against the expected distances.
    - Ensuring the `.mp4` file is created successfully and is playable.

3. **Demo Validation (Addressing Step 7):**
    - We will test the exact required command: `python Ex0.py file.nrrd file.csv file.mp4`.
    - **Validation Criteria:** The script must run end-to-end, the generated MP4 must contain the exact number of frames as the lines in the CSV, and the frames must appear in the exact order of the CSV file.
    - **Performance Testing:** Running the demo on the 500^3 `Synthetic_500.nrrd` to verify it meets the ≥30 FPS benchmark.