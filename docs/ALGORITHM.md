# Main Algorithm Details: 3D to 2D Planar Projection

## 1. Overview
The algorithm computes a 2D image (matrix `E`) representing the projection of a defined plane inside a 3D volumetric matrix (`M`). Instead of iterating over the entire 3D space, it uses a ray-casting/rasterization approach, walking strictly along the plane using normalized 3D vectors to sample the voxel values efficiently.

## 2. Inputs and Initialization
* **Inputs:**
    * `M`: A 3D raster data matrix.
    * A plane defined by 3 points `(a, b, c)`, where `dist(a,b) = dist(a,c)` (isosceles triangle).
* **Distance Calculation:**
  We calculate the lengths of the sides: `Dab = dist(a, b)` and the base `Dbc = dist(b, c)`.
* **Normalized Vectors:**
  We compute normalized vectors (vectors of length 1) to allow step-by-step traversal:
    * `v(ab) = vector(a, b) / Dab`
    * `v(ac) = vector(a, c) / Dab`
* **Output Canvas:**
  We initialize a 2D matrix `E` of dimensions `Dab` (height/rows) by `Dbc` (width/columns).

## 3. The Rasterization Process (Vector Iteration)
The sampling is executed using two nested loops mapping the 3D space to the 2D matrix. We define two "runners", `a1` and `a2`, starting at the apex point `a`.

### Outer Loop (Y-axis / Scanning Rows)
We iterate `y` from `0` to `Dab`. This scans the triangle row by row from top to bottom.
1. `a1` steps 1 unit towards `b`: `a1 = a1 + v(ab)`.
2. `a2` steps 1 unit towards `c`: `a2 = a2 + v(ac)`.
3. We calculate the width of the current row in 3D space: `d12 = dist(a1, a2)`.
4. We define a horizontal normalized step vector for the current row: `dp = vector(a1, a2) / d12`.

### Inner Loop (X-axis / Sampling the Row)
We define a spatial point `p` starting at `a1`. For each row, we iterate a step counter `x1` from `0` to `d12`.
1. **Sampling:** We extract the color/value from the 3D matrix at the current spatial coordinates: `v = M[p]`. (If `p` is out of bounds, `v = 0`).
2. **Centering the 2D Projection:** To ensure the triangle is centered within the rectangular 2D matrix `E` (rather than skewed to the left), we calculate the mapped 2D column index `x`:
   `x = (Dbc / 2) - (d12 / 2) + x1`
3. **Writing:** The sampled value is assigned to the 2D output: `E[x][y] = v`.
4. **Stepping:** Point `p` is advanced by 1 unit along the row in 3D space: `p = p + dp`.