import numpy as np

epsilon = 0.01
def normalize(band):
    band_min, band_max = (np.min(band), np.max(band))
    return ((band-band_min)/((band_max - band_min)))

def brighten(band, alpha=1, beta = 0):
    return np.clip(alpha*band+beta, 0, np.max(band))

def calc_ndvi(NIR, red):
    NIR+=epsilon
    red+=epsilon
    return (NIR - red)/(NIR + red)