import numpy as np
import nrrd
import os

def create_synthetic_nrrd():
    print("Generating 500x500x500 synthetic volume (125 MB)... This might take a few seconds.")

    # 1. הגדרת מידות (500x500x500)
    dims = (500, 500, 500)

    # 2. יצירת מערך של רעש אקראי (uint8 = ערכים בין 0 ל-255)
    volume = np.random.randint(0, 256, size=dims, dtype=np.uint8)

    # 3. הוספת "בלוב" במרכז
    center = 250
    radius = 150
    x, y, z = np.ogrid[:500, :500, :500]
    mask = (x - center)**2 + (y - center)**2 + (z - center)**2 <= radius**2
    volume[mask] = np.clip(volume[mask] + 100, 0, 255)

    # 4. הגדרת נתיב השמירה לתוך תיקיית data
    output_dir = "data"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir) # יוצר את התיקייה אם היא לא קיימת

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

def create_sample_planes_csv():
    print("Generating sample planes.csv...")

    output_dir = "data"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_path = os.path.join(output_dir, "planes.csv")

    csv_content = """# 4 Points: Axial Slices (Full volume width/height)
0, 0, 250, 499, 0, 250, 0, 499, 250, 499, 499, 250
# 4 Points: Coronal Slice (Middle)
0, 250, 0, 499, 250, 0, 0, 250, 499, 499, 250, 499
# 3 Points: Isosceles Triangle (Oblique)
250, 250, 0, 250, 250, 499, 50, 50, 250
"""

    with open(output_path, "w") as f:
        f.write(csv_content)
    print(f"Done! {output_path} created.")

if __name__ == "__main__":
    create_synthetic_nrrd()
    create_sample_planes_csv()