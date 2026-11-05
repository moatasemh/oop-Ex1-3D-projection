# Experiment Results (Assignment Step 8)

## 1. Objective
The goal of this experiment is twofold:
1. **Functional Validation:** To visually verify that the planar projection algorithm correctly samples complex 3D volumetric data (medical and non-medical) and generates playable MP4 videos.
2. **Performance Benchmarking:** To measure the runtime efficiency of the algorithm on a massive 3D volume (500³ bytes = 125,000,000 voxels) and ensure it strictly meets the assignment's performance requirements: **≥30 FPS (Must)** and **100+ FPS (Target)**.

## 2. Experiment Setup
- **Hardware:** ASUS TUF Gaming F15 (Windows 11, 64-bit), Intel Core i7-13620H (2.40 GHz), 32GB RAM
- **Language & Environment:** Python 3.13, Numba (`@njit` JIT compilation), OpenCV.
- **Datasets Used:**
  - **Medical Data:** `MRHead.nrrd` (Real MRI scan).
  - **Food/Complex Scans:** `biscuit_cake.nrrd`, `croissant.nrrd`, `onion.nrrd`, `swiss_roll.nrrd`.
  - **Synthetic Benchmark:** `Synthetic_500.nrrd` (Massive 500x500x500 volume).
  - **Coordinate Sets:** `head.csv`, `biscuit_cake.csv`, `croissant.csv`, `onion.csv`, `swiss_roll.csv`, and `edge_cases.csv`.
---

## 3. Functional Validation (Output Videos)
We executed the system on multiple real-world volumetric datasets to ensure the algorithm correctly samples the 3D space, centers the frames, and assigns `0` to out-of-bounds pixels. 

All generated MP4 files are located in this folder:
- `output_mrhead.mp4`
- `output_biscuit.mp4`
- `output_croissant.mp4`
- `output_onion.mp4`
- `output_swiss.mp4`

![MRHEAD.png](../../../../../OneDrive/%D8%A7%D9%84%D8%B5%D9%88%D8%B1/Screenshots/MRHEAD.png)

---

## 4. Performance Benchmark (500³ Data)
To test the hard performance requirement, we ran the system on the `Synthetic_500.nrrd` dataset. The command used was:
`python Ex0.py data/Synthetic_500.nrrd data/head.csv output_synthetic.mp4`

The system processed 280 planes from the CSV file. To provide a complete picture, we measured two distinct metrics:
1. **Pure Algorithm FPS:** Measures *only* the projection computation (excluding disk I/O and video encoding), as mandated by NFR-01.
2. **End-to-End FPS:** Measures the total time including OpenCV MP4 encoding.

### Results:
- **Canvas Size:** 256x256 (based on the bounding box of the planes in `head.csv`).
- **Total Planes Processed:** 280
- **Pure Algorithm Throughput:** **1623.39 FPS**
- **End-to-End Throughput:** **714.52 FPS**

![FPS_PROOF.png](../../../../../OneDrive/%D8%A7%D9%84%D8%B5%D9%88%D8%B1/Screenshots/FPS_PROOF.png)

---

## 5. Conclusion
The experiment proves that the implementation significantly exceeds the assignment requirements. The integration of Numba (`@njit`) successfully reduced the execution time of the O(H*W) nested loops to C-level speeds. 

Achieving a **Pure Algorithm throughput of over 1600 FPS** on a 500³ volume demonstrates that the algorithmic complexity is highly optimized. Both the mandatory 30 FPS baseline and the 100+ FPS target were passed with exceptional margins, proving the software is both robust and highly efficient.