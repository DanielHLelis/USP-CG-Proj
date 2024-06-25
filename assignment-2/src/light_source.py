import numpy as np


class LightSource:
    position: np.array
    color: np.ndarray
    intensity: float
    decay_coefs = np.ndarray
    def __init__(self,
                 position:np.array,
                 color:np.array = np.array([1.0,1.0,1.0]),
                 intensity:float = 1.0,
                 decay_coefs = np.array([1.0,0,0])
                 ):

        self.position = position
        self.color = color
        self.intensity = intensity
        self.decay_coefs = decay_coefs

    def update(self,dt):
        pass
