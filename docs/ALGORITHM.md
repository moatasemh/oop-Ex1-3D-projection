# Main Algorithm Details: 3D to 2D Planar Projection

## 1. Overview
The algorithm computes a 2D image (matrix `E`) representing the projection of a defined plane inside a 3D volumetric matrix (`M`). Instead of iterating over the entire 3D space (which would be highly inefficient), it uses a dense rasterization approach. By walking strictly along the plane using normalized 3D vectors, it samples the voxel values efficiently in `O(H * W)` time, where `H` and `W` are the dimensions of the output 2D frame.

## 2. Unified Mathematical Formulation (Triangle & Trapezoid)
The assignment defines two plane types: an isosceles triangle (3 points) and an isosceles trapezoid (4 points). Our algorithm uses a **unified two-rail formulation** to handle both seamlessly:

* **3-Point Case (Triangle `a, b, c`):** The start points for both rails are identical (`a1 = a`, `a2 = a`). The distance is `Dab = dist(a,b) = dist(a,c)`, and the base is `Dbc = dist(b,c)`.
* **4-Point Case (Trapezoid `a1, a2, b, c`):** The rails have distinct start points (`a1` and `a2`). The lengths are `D_a1b = dist(a1,b)` and `D_a2c = dist(a2,c)`, which must be equal (within EPS tolerance). The base is `Dbc = dist(b,c)`.

**Initialization:**
1. **Output Matrix:** We initialize a 2D matrix `E` of dimensions `H = round(Dab)` (rows) and `W = round(Dbc)` (columns).
2. **Normalized Vectors:** We compute unit vectors for the left and right rails:
   * `v_left = (b - a1) / D_a1b`
   * `v_right = (c - a2) / D_a2c`

## 3. The Rasterization Process (Vector Iteration)
The sampling uses two nested loops to map the 3D space to the 2D matrix. We define two runners, `curr_left` and `curr_right`, starting at `a1` and `a2`.

### Outer Loop (Y-axis / Scanning Rows)
We iterate `y` from `0` to `H-1` (top to bottom of the projection).
1. Advance the runners by 1 unit along their respective normalized vectors:
   * `curr_left += v_left`
   * `curr_right += v_right`
2. Calculate the width of the current row in 3D space: `d12 = dist(curr_left, curr_right)`.
3. If `d12 < EPS` (e.g., at the apex of a triangle), skip the inner loop to avoid division by zero.
4. Define a horizontal normalized step vector for the current row: `dp = (curr_right - curr_left) / d12`.

### Inner Loop (X-axis / Sampling the Row)
We define a spatial point `p` starting at `curr_left`. We iterate a step counter `x1` from `0` to `floor(d12)`.
1. **Sampling (with Out-of-Bounds Check):** We extract the value from the volume: `v = M[round(p.x)][round(p.y)][round(p.z)]`. If `p` is outside the 3D matrix boundaries, `v = 0` (black).
2. **Centering the 2D Projection:** To ensure the shape is centered within the rectangular matrix `E` (rather than skewed to the left), we calculate the mapped 2D column index `x`:
   `x = floor((W / 2) - (d12 / 2) + x1)`
3. **Writing:** If `x` is within `[0, W-1]`, assign the sampled value: `E[y][x] = v`.
4. **Stepping:** Advance the point along the row: `p += dp`.

## 4. Implementation & Optimization (Runtime Efficiency)
To meet the strict performance requirement (≥30 FPS, target 100+ FPS on a 500³ volume), the algorithm is implemented with the following optimizations:
* **Numba JIT Compilation (`@njit`):** The core nested loops are compiled to native machine code (C-level speed) using Python's Numba library.
* **Zero Object Overhead:** Inside the tight loops, we avoid Python object instantiation. We operate directly on primitive floats and a contiguous NumPy array (`volume_data`).
* **Pre-computation:** All distances (`Dab`, `Dbc`) and normalized vectors (`v_left`, `v_right`) are computed once before the loops begin.

## 5. Complexity Analysis
* **Time Complexity:** `O(H * W)` operations. In the worst case (full square projection), this is `O(N²)` where `N` is the volume width. It does not scale with the depth of the 3D volume, making it highly efficient.
* **Space Complexity:** `O(H * W)` for the output matrix `E`, plus `O(sx * sy * sz)` to store the input 3D volume in RAM.