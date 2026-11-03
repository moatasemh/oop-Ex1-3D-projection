## 1. Introduction

### 1.1 Purpose
This SRS defines the functional and non-functional requirements for a Python CLI tool that projects 2D planes from 3D NRRD volumes into MP4 videos. It serves as the contractual agreement for developers, testers, and the course instructor.

### 1.2 Scope
The system is a standalone backend processing engine. It will:
- Parse 3D volumetric data (NRRD) and geometric plane definitions (CSV).
- Validate shapes (isosceles triangles and trapezoids) using an EPS tolerance of 0.001.
- Execute a vector-stepping projection algorithm using **Numba (`@njit`)** for optimization.
- Render outputs into an MP4 video using OpenCV.
- **Performance Target:** ≥30 FPS (Must) and 100+ FPS (Target) on a 500³ volume.

### 1.3 Definitions
- **NRRD:** Nearly Raw Raster Data (medical imaging format).
- **Voxel:** A 3D pixel.
- **FPS:** Frames Per Second (algorithmic throughput).
- **EPS:** Epsilon tolerance for floating-point comparisons.

---

## 2. Overall Description

### 2.1 Product Perspective
The system is a CLI application accessed via the command line. The design relies on Object-Oriented Principles (Facade, Strategy, Factory patterns) to ensure clean separation of concerns.

### 2.2 Constraints
- **Language:** Python 3.10+
- **Dependencies:** `numpy`, `pynrrd`, `opencv-python`, `numba`.
- **Execution:** Must run exactly as: `python Ex0.py <file.nrrd> <file.csv> <file.mp4>`.

### 2.3 Assumptions
- The NRRD file contains valid 3D data (1 <= sx, sy, sz < 1024).
- The CSV contains rows of 9 (triangle) or 12 (trapezoid) comma-separated numbers.
- Out-of-bounds sampling returns 0 (black pixel).

---

## 3. Specific Requirements

### 3.1 Functional Requirements (FR)
*Designed to be unambiguous, measurable, and traceable.*

- **FR-01 (Data Parsing):** The system shall read `.nrrd` files, supporting raw and GZIP encodings.
- **FR-02 (Normalization):** If the volume is not `uint8`, the system shall normalize it using Min-Max scaling to `uint8` (0-255).
- **FR-03 (CSV Parsing):** The system shall parse rows of 9 or 12 numbers, ignoring empty lines and comments.
- **FR-04 (Geometry Validation):** The system shall validate:
  - 3-point: `|dist(a,b) - dist(a,c)| < 0.001`.
  - 4-point: `|dist(a1,b) - dist(a2,c)| < 0.001` and `dist(a1,a2) <= dist(b,c) + 0.001`.
- **FR-05 (Algorithm):** The system shall compute projections by stepping along normalized 3D vectors `v(ab)` and `v(ac)` as defined in the assignment.
- **FR-06 (Boundaries):** Any sampled point `(x, y, z)` outside the matrix boundaries shall be assigned `0`.
- **FR-07 (Canvas):** The system shall center each 2D frame on a black canvas of the maximum calculated width/height.
- **FR-08 (Video):** The system shall generate a single `.mp4` video with one frame per valid CSV row, in sequential order.
- **FR-09 (CLI):** The system shall execute via the exact CLI format specified in the constraints.

### 3.2 Non-Functional Requirements (NFR)
- **NFR-01 (Performance):** Algorithmic throughput (excluding video encoding) must be **≥30 FPS** on a 500³ volume, targeting **100+ FPS**.
- **NFR-02 (Stability):** Invalid CSV rows (geometrically impossible) must be skipped gracefully with a warning, without crashing.
- **NFR-03 (Design):** The system shall implement **Facade**, **Strategy** (`ProjectablePlane`), and **Factory** (`ShapeFactory`) design patterns.

---

## 4. Appendices

### 4.1 Use Case: Execute Projection
- **Actor:** Developer / User.
- **Precondition:** Python dependencies installed; valid NRRD and CSV files exist.
- **Main Flow:**
  1. User executes `python Ex0.py data.nrrd planes.csv output.mp4`.
  2. System loads and normalizes the NRRD volume.
  3. System parses CSV and validates shapes.
  4. System iterates through planes, running the projection algorithm.
  5. System centers frames and writes to `output.mp4`.
  6. System prints final FPS.
- **Alternative Flow (Invalid Shape):** If a CSV row violates EPS rules, the system prints a warning, skips the row, and continues.
- **Postcondition:** A playable `.mp4` is generated.

### 4.2 Traceability Matrix
| Assignment Step | SRS Requirement | Component / Class |
| :--- | :--- | :--- |
| Read NRRD | FR-01, FR-02 | `NrrdReader.py` |
| Parse CSV | FR-03, FR-04 | `ShapeFactory.py`, `Ex0.py` |
| Algorithm | FR-05, FR-06 | `ProjectionEngine.py` |
| Video Output | FR-07, FR-08 | `OpenCvVideoWriter.py` |
| CLI / Demo | FR-09 | `Ex0.py` |
| Performance | NFR-01 | `ProjectionEngine.py` (`@njit`) |