from owslib.wms import WebMapService
from owslib.wfs import WebFeatureService

import numpy as np
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


def get_map(wms, layer, raster, bbox, export_folder, styles='default', srs='EPSG:2180'):

    resp = wms.getmap(
        layers=[layer],
        styles=[styles],
        srs=srs,
        bbox=np.fromstring(bbox, dtype=float, sep=','),
        size=raster['size'],
        format=raster['format']
    )

    out = open(os.path.join(export_folder, 'resp_map.' + raster['extension']), 'wb')
    out.write(resp.read())
    out.close()

    return resp


def get_center_tile(wms, layer, raster, bbox, export_folder, styles='default', srs='EPSG:2180'):
    resp = wms.getfeatureinfo(
        layers=[layer],
        styles=[styles],
        srs=srs,
        bbox=np.fromstring(bbox, dtype=float, sep=','),
        size=raster['size'],
        format=raster['format'],
        query_layers=[layer],
        xy=tuple([x/2 for x in raster['size']])
    )

    out = open(os.path.join(export_folder, 'resp_gfi.html'), 'wb')
    out.write(resp.read())
    out.close()

    return resp
