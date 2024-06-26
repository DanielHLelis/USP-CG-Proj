import numpy as np


class LightSource:
    position: np.ndarray
    color: np.ndarray
    intensity_d: float
    intensity_s: float
    decay_coefs = np.ndarray

    def __init__(
        self,
        position: np.ndarray,
        color: np.ndarray = np.array([1.0, 1.0, 1.0]),
        intensity_d: float = 1.0,
        intensity_s: float = 1.0,
        decay_coefs=np.array([1.0, 0, 0]),
    ):

        self.position = position
        self.color = color
        self.intensity_d = intensity_d
        self.intensity_s = intensity_s
        self.decay_coefs = decay_coefs
