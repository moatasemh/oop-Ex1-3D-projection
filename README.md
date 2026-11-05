# Ex1: 3D Volume Planar Projection (Intro to Software Engineering)

**Author:** Moatasem · **Course:** OOP/OOD · **Language:** Python 3

## Problem Definition
Given a 3D raster data matrix (M) representing volumetric data (e.g., an MRI scan), and a plane (p) defined by 3 or 4 co-planar points, the objective is to compute a 2D matrix (image) representing the projection of that plane within the volume. 

The problem is intentionally under-specified. This project provides a robust design that validates the input geometry, computes the necessary 3D vectors, and efficiently samples the volume to generate a 2D frame. The outputs are compiled into an MP4 video.

## Project Scope
- **Data Parsing:** Reading 3D volumetric data (NRRD format) and parsing plane coordinates from CSV files.
- **Geometric Validation:** Verifying that 3 or 4 points form a valid isosceles triangle or trapezoid (using an EPS tolerance).
- **Algorithmic Core:** Implementing the vector-stepping planar rasterization algorithm defined in the assignment.
- **Performance:** Achieving high runtime efficiency. Given a matrix of size 500³ bytes, the target is ≥30 FPS (Must) and 100+ FPS (Target). The implementation uses **Numba (`@njit`)** to compile the core algorithm to C-level machine code, achieving **178+ FPS**.
- **Video Generation:** Normalizing the 3D volume to 8-bit grayscale and compiling the sequence of computed 2D projection frames into a final MP4 video using **OpenCV**.

## Repository Layout
- `Ex0.py` — The assignment entry point. Acts as a wrapper/router that forwards commands to `Main.py` to ensure proper execution from the root directory.
- `conftest.py` — Pytest configuration file ensuring `src` modules are found during testing.
- `tests/` — Automated test suite verifying geometry, engine performance, and robustness.
  - `test_geometry.py` — Unit tests for triangle/trapezoid creation and EPS validation.
  - `test_engine.py` — Tests for out-of-bounds sampling and 500³ FPS performance.
  - `test_epsilon_sensitivity.py` — Tests coordinate shift sensitivity and EPS bounds.
  - `test_reader.py` — Tests error handling for missing NRRD files.
- `src/` — Source code files.
  - `Main.py` — The main entry point (Facade Pattern).
  - `NrrdReader.py` — Handles NRRD parsing and normalization.
  - `ProjectionEngine.py` — The core projection algorithm (optimized with Numba).
  - `ProjectablePlane.py` — Abstract base class for shapes (Strategy Pattern).
  - `IsoscelesTriangle.py` — 3-point plane implementation.
  - `IsoscelesTrapezoid.py` — 4-point plane implementation.
  - `ShapeFactory.py` — Factory Pattern to instantiate shapes from CSV data.
  - `OpenCvVideoWriter.py` — Handles MP4 generation and frame centering.
- `docs/` — Documentation.
  - `SRS.md` — Software Requirements Specification.
  - `ALGORITHM.md` — Detailed algorithm breakdown.
  - `EXPERIMENT.md` — Performance benchmark results.
- `data/` — NRRD datasets and CSV coordinate lists.
- `tools/` — Utility scripts for testing and benchmarking.
  - `generate_data.py` — Generates a massive 500x500x500 synthetic NRRD volume (with a central spherical blob) to benchmark and prove the 100+ FPS requirement, keeping the project independent of heavy external files.


## Dataset
The project includes a diverse dataset of NRRD files and corresponding CSV coordinate sets, tested and validated. The data is divided into volumetric scans and geometric test cases:

### 📦 Volumetric Data (NRRD Files)
* **MRHead.nrrd** (6,735 KB): Real MRI medical data obtained from 3D Slicer sample data. Used for visual demonstration and standard testing.
* **Synthetic_500.nrrd** (122,071 KB): A massive generated 500x500x500 volume. Used specifically to benchmark and prove the ≥30 FPS and 100+ FPS performance requirements.
* **croissant.nrrd** (61,525 KB): High-resolution scan of a croissant for complex non-medical shape projection.
* **swiss_roll.nrrd** (14,784 KB): Medium-resolution scan of a Swiss roll cake.
* **biscuit_cake.nrrd** (8,927 KB): Scan of a biscuit cake, used for testing distinct geometric planes.
* **onion.nrrd** (4,760 KB): A smaller scan of an onion for rapid testing.

### 🎯 Coordinate Sets (CSV Files)
The CSV files define the planes to be projected. Each line represents a plane and follows this strict format:
*   The first number indicates the number of points (`3` for a triangle, `4` for a trapezoid).
*   Followed by the X, Y, Z coordinates for each point.
*   Example (Triangle): `3, 0,0,0, 100,0,0, 0,100,0`
*   Example (Trapezoid): `4, 0,0,0, 100,0,0, 0,100,0, 100,100,0`

*Here is the list of the provided coordinate sets:*
* **head.csv**: Standard geometric test cases designed to work with the MRHead medical scan.
* **croissant.csv**: Coordinate planes tailored specifically for the croissant volume.
* **biscuit_cake.csv**: Coordinate planes tailored for the biscuit cake volume.
* **edge_cases.csv**: A dedicated coordinate file designed to stress-test the geometric validation logic (e.g., collinear points, invalid triangles, and broken trapezoids).
* **swiss_roll.csv**: Coordinate planes tailored specifically for the Swiss roll cake volume.
* **onion.csv**: Coordinate planes tailored for the onion volume.
## Design Patterns & OOP Architecture
To ensure a clean and extensible design, the project heavily utilizes Object-Oriented principles:
- **Facade Pattern:** `Ex0.py` provides a simple interface, hiding the complex orchestration between the reader, engine, and video writer.
- **Strategy Pattern:** `ProjectablePlane` acts as an interface, allowing `IsoscelesTriangle` and `IsoscelesTrapezoid` to define their own geometric parameters.
- **Factory Pattern:** `ShapeFactory` dynamically creates the appropriate shape object based on the CSV input.

## Setup & Usage

### Prerequisites
Make sure you have Python installed, then install the required libraries:
```bash
pip install numpy pynrrd opencv-python numba
pip install pytest

```

### Running the Automated Tests (Testing Strategy)
The project includes a robust test suite built with `pytest`, verifying three core principles: Maintainability, Robustness, and Efficiency.
To run all tests (from the root directory), execute:
```bash
python -m pytest -v tests/