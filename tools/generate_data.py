import numpy as np
import nrrd
import os

def create_synthetic_nrrd():
    print("Generating 500x500x500 synthetic volume (125 MB)... This might take a few seconds.")

    # 1.  (500x500x500)
    dims = (500, 500, 500)


    volume = np.random.randint(0, 256, size=dims, dtype=np.uint8)


    center = 250
    radius = 150
    x, y, z = np.ogrid[:500, :500, :500]
    mask = (x - center)**2 + (y - center)**2 + (z - center)**2 <= radius**2
    volume[mask] = np.clip(volume[mask] + 100, 0, 255)


    output_dir = "data"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_path = os.path.join(output_dir, "Synthetic_500.nrrd")

    header = {
        'type': 'uchar',
        'dimension': 3,
        'sizes': [500, 500, 500],
        'encoding': 'raw',
        'endian': 'little'
    }

    print(f"Saving to {output_path}...")
    nrrd.write(output_path, volume, header)
    print("Done! Synthetic data ready for benchmarking.")



if __name__ == "__main__":
    create_synthetic_nrrd()
