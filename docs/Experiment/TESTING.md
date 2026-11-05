# Testing Strategy & Test Plan (Assignment Step 5)

Our testing strategy is built on three core software engineering principles, as defined in the course requirements: **Efficiency, Robustness, and Maintainability**. To prove our system adheres to these principles, we implemented an automated test suite using `pytest`.

## 1. Efficiency (יעילות)
*Goal:* Prove the system handles massive 3D volumes within the strict performance requirements (≥30 FPS).
*Implementation:* The `test_engine.py` file contains `test_fps_requremnts()`, which generates a simulated 500x500x500 volume in memory and runs the projection algorithm using a 256x256 plane. It uses `time.perf_counter()` to measure throughput.
*Proof:* The test asserts that the resulting FPS is strictly greater than 30. If a future code change slows down the system (e.g., accidentally removing the Numba `@njit` decorator), this test will immediately fail.

## 2. Robustness & Edge Cases (עמידות בביקוש)
*Goal:* Ensure the system does not crash when faced with extreme, invalid, or out-of-bounds inputs.
*Implementation:* 
- `test_engine.py / test_out_of_bounds`: Feeds the engine a plane that exists completely outside the 3D matrix. The system must return a black frame (value 0) rather than throwing an IndexError.
- `test_reader.py`: Verifies that trying to load a missing NRRD file throws a clean `FileNotFoundError`.
- `test_geometry.py / test_invalid_triangle_not_isosceles`: Feeds points that cannot form a valid shape and asserts that a `ValueError` is raised.

## 3. Maintainability & Bug Detection (תחזוקה)
*Goal:* If a developer accidentally introduces a bug or breaks a geometric formula, the system must immediately catch it.
*Implementation:* We wrote strict Unit Tests for the geometry classes and the Factory pattern.
- `test_geometry.py`: Checks that `ShapeFactory` correctly instantiates a Triangle for 9 coordinates and a Trapezoid for 12 coordinates.
- `test_epsilon_sensitivity.py`: **Sensitivity Test** - Shifts a plane coordinate by exactly `0.0005` (within EPS) and `0.005` (outside EPS) to ensure the validation logic triggers correctly. It also ensures that a microscopic shift in coordinates actually changes the output image matrix (`np.sum(frame_original != frame_shifted) > 0`).