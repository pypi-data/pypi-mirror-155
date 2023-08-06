from typing import Optional, Tuple
from openride import Viewer
import numpy as np
import vtk
from vtk.util.numpy_support import vtk_to_numpy
import cv2
import skvideo.io


def get_last_rendered_image(viewer: Viewer) -> np.ndarray:
    win_to_img = vtk.vtkWindowToImageFilter()
    win_to_img.SetShouldRerender(0)
    win_to_img.SetInput(viewer.renderWindow)
    win_to_img.Update()
    vtk_image = win_to_img.GetOutput()

    flip = vtk.vtkImageFlip()
    flip.SetInputData(vtk_image)
    flip.SetFilteredAxis(1)
    flip.FlipAboutOriginOn()
    flip.Update()
    vtk_image = flip.GetOutput()

    width, height, _ = vtk_image.GetDimensions()
    vtk_array = vtk_image.GetPointData().GetScalars()
    components = vtk_array.GetNumberOfComponents()
    return vtk_to_numpy(vtk_array).reshape(height, width, components)


class Recorder:
    def __init__(self, viewer: Viewer, output_file: str, fps: int = 60, resolution: Optional[Tuple[int, int]] = None):

        self.viewer = viewer
        self.viewer.set_callback(self.update)
        self.resolution = resolution

        self.video_writer = skvideo.io.FFmpegWriter(
            output_file, inputdict={"-r": str(fps)}, outputdict={"-r": str(fps)}
        )

    def update(self):

        image = get_last_rendered_image(self.viewer)

        if not self.resolution:
            self.resolution = (image.shape[0], image.shape[1])

        if (image.shape[0], image.shape[1]) != self.resolution:
            image = cv2.resize(image, self.resolution)

        self.video_writer.writeFrame(image)

    def close(self):
        self.video_writer.close()
