import numpy as np
import nrrd
from Volume3D import Volume3D
class NrrdReader:
    @staticmethod
    def load(filepath: str) -> Volume3D:
        print(f"[Volume Manager] Loading NRRD from {filepath}...")
        data, header = nrrd.read(filepath)

        if data.dtype != np.uint8:
            vol_min, vol_max = data.min(), data.max()
            if vol_max == vol_min:
                data = np.zeros_like(data, dtype=np.uint8)
            else:
                data = ((data - vol_min) / (vol_max - vol_min) * 255).astype(np.uint8)
            """
 This uses Min-Max Scaling to compress all pixel values into a 0 to 1 range by subtracting the minimum and dividing by the total range.
 The result is multiplied by 255 and cast to an 8-bit integer (np.uint8) to match standard grayscale video requirements.
 NumPy executes this mathematical calculation as a vectorized operation across the entire 3D array simultaneously, making it extremely fast.
            """
        return Volume3D(data)