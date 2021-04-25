from itertools import product

from osgeo import osr
from osgeo import gdal

import matplotlib.image as mpimg
import numpy as np
import time
import os

from src.get_from_wms_or_wfs import get_data, get_map


def run(export_folder):
    box0, box1, box2, box3 = box = np.fromstring('299000,446000,299100,446100', dtype=float, sep=',')

    tile = 200
    size = (box[2] - box[0])
    resolution = size / tile

    wms = get_data('https://mapy.geoportal.gov.pl/wss/service/PZGIK/ORTO/WMS/StandardResolution', 0, '1.3.0')

    for i in range(4):
        box0, box2 = (box[0], box[2])
        for j in range(4):
            raster = {
                'name': f'tile_{i}{j}',
                'extension': 'jpeg',
                'size': (tile,)*2,
                'format': 'image/jpeg'
            }

            get_map(wms, 'Raster', raster, f'{box1},{box0},{box3},{box2}', export_folder)
            img = mpimg.imread(os.path.join(export_folder, f"{raster['name']}.{raster['extension']}"))

            dst_ds = gdal.GetDriverByName('GTiff').Create(
                os.path.join(export_folder, f"{raster['name']}.tif"),
                tile, tile, 3, gdal.GDT_Byte
            )

            dst_ds.SetGeoTransform((box1, resolution, 0, box2, 0, -resolution))

            srs = osr.SpatialReference()
            srs.ImportFromEPSG(2180)

            dst_ds.SetProjection(srs.ExportToWkt())
            for k in range(3):
                dst_ds.GetRasterBand(k+1).WriteArray(img[:, :, k])
            dst_ds.FlushCache()
            dst_ds = None

            box0 += size
            box2 += size
            time.sleep(2)

        box1 += size
        box3 += size

    tif_files = [f"{export_folder}/tile_{el[0]}{el[1]}.tif" for el in product(range(4), repeat=2)]
    vrt = gdal.BuildVRT(os.path.join(export_folder, "zad03_merged.vrt"), tif_files)
    gdal.Translate(os.path.join(export_folder, "zad03_merged.tif"), vrt, xRes=resolution, yRes=-resolution)
    vrt = None

    os.remove(os.path.join(export_folder, "zad03_merged.vrt"))
    for i in tif_files:
        os.remove(i)
        os.remove(i.replace("tif", "jpeg"))
