import sys
import time
from ShapeFactory import ShapeFactory
from ProjectionEngine import ProjectionEngine
from OpenCvVideoWriter import OpenCvVideoWriter
from NrrdReader import NrrdReader
import os
def resolve_input_path(filepath: str) -> str:

    if os.path.exists(filepath):
        return filepath

    # check if the in data file
    data_path = os.path.join("data", filepath)
    if os.path.exists(data_path):
        return data_path

    return filepath
def main(): #facade design pattern
    if len(sys.argv) < 4:
        print("Usage: python main.py <file.nrrd> <file.csv> <file.mp4>")
        sys.exit(1)

    nrrd_file = resolve_input_path(sys.argv[1])
    csv_file = resolve_input_path(sys.argv[2])
    mp4_file = sys.argv[3]

    # 1 (Volume Manager)
    volume = NrrdReader.load(nrrd_file)

    # 2 CSV (Geometry Factory)
    planes = []
    print(f" Parsing shapes from {csv_file}...")
    with open(csv_file, 'r') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            try:
              # spliting the lines to parts
                raw_parts = line.split(',')

                # pass the last empty parts in the line
                if len(raw_parts) < 10:
                    continue


                parts = [float(x) for x in raw_parts if x.strip() != '']

                # how many points
                num_points = int(parts[0])


                if num_points == 3:
                    coords = parts[1:10]  # taking the first 9 cordenats
                elif num_points == 4:
                    coords = parts[1:13]
                else:
                    print(f"[Warning] Unknown number of points ({num_points}) on row {line_num}")
                    continue

                try:
                    shape = ShapeFactory.create_shape(coords)
                    planes.append(shape)
                except ValueError as geo_err:
                    print(f"[Warning] Geometry error on row {line_num}: {geo_err}")
            except ValueError:
            # An elegant handling of the title row (text cannot become a float)
                print(f" Skipping header text on row {line_num}")
            except Exception as e:
                # Handle any other unexpected errors
                print(f"[Warning] Skipping invalid shape on row {line_num}: {e}")

    if not planes:
        print(" No valid planes parsed. Exiting.")
        sys.exit(1)

    # Finding the maximum dimensions for the video canvas
    max_w = max([p.W for p in planes])
    max_h = max([p.H for p in planes])
    if max_w % 2 != 0: max_w += 1
    if max_h % 2 != 0: max_h += 1

    # 3 (Engine & Video Exporter)
    engine = ProjectionEngine()
    video_exporter = OpenCvVideoWriter(mp4_file, max_w, max_h)

    # 4. Orchestration: iterating over the planes, processing, and saving
    if len(planes) > 0:
        engine.project(volume, planes[0])
    print(f" Processing {len(planes)} shapes...")
    total_algo_time = 0.0
    total_e2e_time = 0.0
    for i, plane in enumerate(planes, 1):
        # running the algorithm
        t0 = time.perf_counter() # Measure ONLY algorithm execution
        t_start_e2e=time.perf_counter() # Start measuring End-to-End (Total time)
        projected_frame = engine.project(volume, plane)
        total_algo_time += (time.perf_counter() - t0)
        # saving the video
        video_exporter.add_frame(projected_frame)
        total_e2e_time += (time.perf_counter() - t_start_e2e)
        print(f" -> Processed plane {i}/{len(planes)}")

    video_exporter.release()
    algo_fps = len(planes) / total_algo_time if total_algo_time > 0 else 0
    e2e_fps = len(planes) / total_e2e_time if total_e2e_time > 0 else 0
    print(f"Done! Video saved to: {mp4_file}")
    print(f"Pure Algorithm FPS = {algo_fps:.2f}")
    print(f"End to End FPS = {e2e_fps:.2f} -> algo+ Video Encoding")

if __name__ == "__main__":
    main()