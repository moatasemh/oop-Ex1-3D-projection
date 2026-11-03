
import numpy as np
import cv2
from VideoWriter import VideoWriter


class OpenCvVideoWriter(VideoWriter):
    def __init__(self, filepath: str, max_w: int, max_h: int, fps: float = 10.0):
        self.fps = fps
        self.max_w = max_w
        self.max_h = max_h
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.writer = cv2.VideoWriter(filepath, fourcc, fps, (max_w, max_h), isColor=False)
        print(f"[Video Exporter] Initialized Canvas size: {max_w}x{max_h} at {fps} FPS")

    def add_frame(self, frame: np.ndarray):
        canvas = np.zeros((self.max_h, self.max_w), dtype=np.uint8)

        # Centering the frame on the maximum canvas
        offset_y = (self.max_h - frame.shape[0]) // 2
        offset_x = (self.max_w - frame.shape[1]) // 2
        canvas[offset_y:offset_y + frame.shape[0], offset_x:offset_x + frame.shape[1]] = frame

        # Writing the frame

        self.writer.write(canvas)

    def release(self):
        self.writer.release()
        print("[Video Exporter] Video rendering complete.")