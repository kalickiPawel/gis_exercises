from owslib.wms import WebMapService
from owslib.wfs import WebFeatureService
from itertools import product

from osgeo import osr
from osgeo import gdal

import matplotlib.image as mpimg
import numpy as np
import time
import os


def get_data(url, wfs, v):
    """
    This function makes it possible to download data
    via WMS and WFS services.
    :param url: address of service
    :param wfs: 0 - wms, 1 - wfs
    :param v: service version
    :return: wms or wfs object
    """
    if not wfs:
        wms = WebMapService(url, version=v) if v is not None else WebMapService(url)
        print(f"{wms.identification.type} {wms.identification.version}")
        print(f"Title: {wms.identification.title}")
        print(f"Abstract: {wms.identification.abstract}")
        print(f"List of contents: {list(wms.contents)}")
        return wms
    else:
        wfs = WebFeatureService(url, version=v) if v is not None else WebFeatureService(url)
        print(f"{wfs.identification.type} {wfs.identification.version}")
        print(f"Title: {wfs.identification.title}")
        print(f"Abstract: {wfs.identification.abstract}")
        print(f"List of contents: {list(wfs.contents)}")
        return wfs


def get_layer(service, layer):
    """
    Get information from WMS or WFS for specific layer
    :param service: WMS or WFS service object
    :param layer: name of layer in service
    :return: service of layer, name of dataset
    """
    print(f"Dataset name: {service[layer].title}")
    print(f"CRS: {service[layer].crsOptions}")
    return service[layer], service[layer].title.replace(" ", "_").lower()


def get_map(service, layer, raster, bbox, export_folder, styles='default', srs='EPSG:2180'):
    """
    Get map from WMS or WFS for specific bbox and resolution
    :param service: WMS or WFS service object
    :param layer: name of layer in service
    :param raster: dictionary with 'name', 'size', 'format' and 'extension' of raster
    :param bbox: bbox format in string
    :param export_folder: name of export data folder
    :param styles: string of styles of map
    :param srs: specific CRS
    :return: response from service
    """
    resp = service.getmap(
        layers=[layer],
        styles=[styles],
        srs=srs,
        bbox=np.fromstring(bbox, dtype=float, sep=','),
        size=raster['size'],
        format=raster['format']
    )

    out = open(os.path.join(export_folder, raster['name'] + '.' + raster['extension']), 'wb')
    out.write(resp.read())
    out.close()

    return resp


def get_center_tile(service, layer, raster, bbox, export_folder, styles='default', srs='EPSG:2180'):
    """
    Get WMS or WFS information from center the tile
    :param service: WMS or WFS service object
    :param layer: name of layer in service
    :param raster: dictionary with 'name', 'size', 'format' and 'extension' of raster
    :param bbox: bbox format in string
    :param export_folder: name of export data folder
    :param styles: string of styles of map
    :param srs: specific CRS
    :return: response from service
    """
    resp = service.getfeatureinfo(
        layers=[layer],
        styles=[styles],
        srs=srs,
        bbox=np.fromstring(bbox, dtype=float, sep=','),
        size=raster['size'],
        format=raster['format'],
        query_layers=[layer],
        xy=tuple([x/2 for x in raster['size']])
    )

    out = open(os.path.join(export_folder, raster['name'] + '.html'), 'wb')
    out.write(resp.read())
    out.close()

    return resp


def get_tiles(service, num_of_tiles, tile, bbox, export_folder, name):
    """
    Get GeoTiff file from WMS or WFS service,
    for specific bbox, resolution and num of tiles
    :param service: WMS or WFS service object
    :param num_of_tiles: number of tiles
    :param tile: size of one tile
    :param bbox: bbox format in string
    :param export_folder: name of export data folder
    :param name: name of export tiff file
    :return: None
    """
    box0, box1, box2, box3 = box = np.fromstring(bbox, dtype=float, sep=',')
    size = (box[2] - box[0])
    res = size / tile

    for i in range(num_of_tiles):
        box0, box2 = (box[0], box[2])
        for j in range(num_of_tiles):
            raster = {
                'name': f'tile_{i}{j}',
                'extension': 'jpeg',
                'size': (tile,) * 2,
                'format': 'image/jpeg'
            }

            get_map(service, 'Raster', raster, f'{box1},{box0},{box3},{box2}', export_folder)
            img = mpimg.imread(os.path.join(export_folder, f"{raster['name']}.{raster['extension']}"))

            dst_ds = gdal.GetDriverByName('GTiff').Create(
                os.path.join(export_folder, f"{raster['name']}.tif"),
                tile, tile, 3, gdal.GDT_Byte
            )

            dst_ds.SetGeoTransform((box1, res, 0, box2, 0, -res))

            srs = osr.SpatialReference()
            srs.ImportFromEPSG(2180)

            dst_ds.SetProjection(srs.ExportToWkt())
            for k in range(3):
                dst_ds.GetRasterBand(k + 1).WriteArray(img[:, :, k])
            dst_ds.FlushCache()
            dst_ds = None

            box0 += size
            box2 += size
            time.sleep(2)

        box1 += size
        box3 += size

    tif_files = [f"{export_folder}/tile_{el[0]}{el[1]}.tif" for el in product(range(num_of_tiles), repeat=2)]
    vrt = gdal.BuildVRT(os.path.join(export_folder, f"{name}_merged.vrt"), tif_files)
    gdal.Translate(os.path.join(export_folder, f"{name}_merged.tif"), vrt, xRes=res, yRes=-res)
    vrt = None

    os.remove(os.path.join(export_folder, f"{name}_merged.vrt"))
    for i in tif_files:
        os.remove(i)
        os.remove(i.replace("tif", "jpeg"))

    return None
