from dataclasses import dataclass, fields
from typing import List

import numpy as np

# https://support.pix4d.com/hc/en-us/articles/202558969-Yaw-Pitch-Roll-and-Omega-Phi-Kappa-angles

@dataclass
class InternalParams:
    camera_calibration_file: int
    sensor_width_w: np.float64
    sensor_width_l: np.float64
    image_size_w_pix: np.float64
    image_size_l_pix: np.float64
    focal: np.float64
    xpoff_mm: np.float64
    ypoff_mm: np.float64
    xpoff_pix: np.float64
    ypoff_pix: np.float64

@dataclass
class CameraParams:
    fileName: str
    imageWidth: np.uint16
    imageHeight: np.uint16
    camera_matrix_K: np.array           # camera matrix K [3x3]
    radial_distortion: np.array         # radial distortion [3x1]
    tangential_distortion: np.array     # tangential distortion [2x1]
    camera_position_t: np.array         # camera position t [3x1]
    camera_rotation_R: np.array         # camera rotation R [3x3]
    camera_model_m: np.array            # camera model m = K [R|-Rt] X

@dataclass
class ExternalCameraParams:
    imageName: str
    X: np.float64
    Y: np.float64
    Z: np.float64
    Omega: np.float64   # roll
    Phi : np.float64    # pitch
    Kappa: np.float64   # yaw

@dataclass
class Pix4DInternalCameraParams:
    camera_calibration_file: int
    #Focal Length mm assuming a sensor width of 12.83331744000000007588x8.55554496000000064271mm
    F: np.float64
    #Principal Point mm
    Px: np.float64
    Py: np.float64
    #Symmetrical Lens Distortion Coeffs
    K1: np.float64
    K2: np.float64
    K3: np.float64
    #Tangential Lens Distortion Coeffs
    T1: np.float64
    T2: np.float64

@dataclass
class Camera:
    focal_length: np.float64
    ppac: List[np.float64]
    ppbs: np.float64
    film_format: np.float64
    lens_distortion_flag: str
    io_required: str
    camera_type: str
    media_type: str
    pixel_size: List[np.float64] #probably in nanometers
    image_size_in_pixels: np.float64
    scanline_orientation: np.float64
    photo_coord_sys_orientation: np.float64
    photo_coord_sys_origin: np.float64
    focal_length_calibration_flag: str
    calibrated_focal_length_stddev: np.float64
    ppac_calibration_flag: str
    calibrated_ppac_stddevs: np.float64
    self_calibration_enabled_params: np.float64
    antenna_offsets: np.float64

@dataclass
class PMatrix:
    fileName: str
    pmatrix: np.array
