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
            data = ((data - vol_min) / (vol_max - vol_min) * 255).astype(np.uint8)
        return Volume3D(data)