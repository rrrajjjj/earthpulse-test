from fastapi import FastAPI, Path, Response
import rasterio
import numpy as np 
from PIL import Image
import io
import os
from utils import calc_ndvi, normalize, brighten


app = FastAPI()

@app.get("/")
def home():
    return ("There are 3 endpoints in this API:\
            1. /attributes/filename: returns metadata for the file\
            2. /thumbnail/filename: returns an rgb image as png \
            3. /ndvi/filename: return ndvi calculated on the image as png")

@app.get("/attributes/{filename}")
def get_attributes(filename:str = Path(None, description="The filename of the image")):
    attributes = dict()
    with rasterio.open(filename) as dataset:
        attributes["image_size"] = {"width":dataset.width, 
                                    "height": dataset.height}
        attributes["num_bands"] = dataset.count
        attributes["crs"] = str(dataset.crs)
        attributes["bounding_box"] = (dataset.bounds)
    return attributes
    

@app.get("/thumbnail/{filename}")
def get_thumbnail(filename:str = Path(None, description="The filename of the TIFF image")):
    with rasterio.open(filename) as dataset:

        r, g, b = dataset.read(4), dataset.read(3), dataset.read(2)

        # preprocessing
        r, g, b = [brighten(band, alpha=2) for band in [r, g, b]]
        r, g, b = [normalize(band) for band in [r, g, b]]

        # combine channels
        img_np = (np.dstack((r,g,b))*255).astype(np.uint8)
        img = Image.fromarray(img_np)

        # render as png
        with io.BytesIO() as buf:
            img.save(buf, format='PNG')
            im_bytes = buf.getvalue()
        
    return Response(im_bytes, media_type='image/png')


@app.get("/ndvi/{filename}")
def get_ndvi(filename:str = Path(None, description="The filename of the TIFF image")):
    with rasterio.open(filename) as dataset:
        NIR = dataset.read(8).astype(np.float)
        red = dataset.read(4).astype(np.float)
        ndvi = calc_ndvi(NIR, red)
        ndvi = normalize(ndvi)
        ndvi = Image.fromarray(((ndvi*255).astype(np.uint8)))

        # render as png
        with io.BytesIO() as buf:
            ndvi.save(buf, format='PNG')
            im_bytes = buf.getvalue()
        
    return Response(im_bytes, media_type='image/png')
