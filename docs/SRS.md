# Software Requirements Specification (SRS)
**Project:** Ex1 — Planar Projection of 3D Volumetric Data
**Course:** Introduction to Software Engineering (OOP/OOD)

## 1. Introduction
This document defines the requirements for a software tool that projects a plane (defined by 3 or 4 points) from a 3D volumetric matrix (NRRD file) onto a 2D image matrix. The outputs are compiled into an MP4 video.

## 2. Functional Requirements
* **Data Reading:** The system shall read 3D raster data from standard NRRD files (e.g., MRHead.nrrd).
* **Coordinates Parsing:** The system shall read a CSV file containing rows of coordinates representing planes (3 points for a triangle, 4 points for a trapezoid).
* **Projection Algorithm:** For each plane, the system shall compute normalized vectors and sample the 3D volume using the step-by-step vector iteration algorithm defined in the project specifications.
* **Out-of-Bounds:** If a sampled point in the plane falls outside the 3D matrix boundaries, its value shall be 0.
* **Video Generation:** The system shall generate a single MP4 video file, where each frame corresponds to a computed 2D projection plane from the CSV in sequential order.
* **CLI Execution:** The program shall run via command line exactly as: `python Ex0.py <file.nrrd> <file.csv> <file.mp4>`.

## 3. Non-Functional Requirements
* **Performance:** The algorithm must run at a minimum of 30 FPS, with a target of 100+ FPS for a 500^3 byte matrix.
* **Precision:** Geometric validations (e.g., distance comparisons) must use an EPS tolerance of 0.001.
* **Design:** The system shall be implemented in Java using solid Object-Oriented Design (OOD) principles.

## 4. Inputs and Outputs
* **Inputs:**
    1. A volumetric data file (`.nrrd`).
    2. A coordinates list (`.csv`).
* **Output:** A video file (`.mp4`) containing the generated frames.

## 5. Data Set
To fulfill the requirements, the project uses the following datasets:
1. **Primary Real Data (`MRHead.nrrd`):**
    - **Source:** 3D Slicer open-source sample data.
    - **Dimensions:** 256 x 256 x 130.
    - **Data Type:** uint8 (unsigned 8-bit integer).
    - **Purpose:** Used to validate the algorithm on real MRI data and generate the final demo video.
2. **Performance Benchmark Data (`synthetic_500.nrrd`):**
    - **Source:** Generated locally via a script.
    - **Dimensions:** 500 x 500 x 500 (exactly 500^3 bytes).
    - **Data Type:** uint8.
    - **Purpose:** Specifically designed to measure throughput and prove the algorithm meets the ≥30 FPS requirement (as the MRHead is smaller than 500^3).
3. **Coordinate Files (`.csv`):**
    - Contains various plane definitions: axial slices (4 points), oblique triangles (3 points), and edge cases that fall outside the volume boundaries.