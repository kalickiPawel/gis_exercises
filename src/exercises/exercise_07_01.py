from owslib.fes import Or, PropertyIsEqualTo, etree

import subprocess
import os

from src.get_from_wms_or_wfs import get_data, get_layer


def run(export_folder):
    print("-->Started exercise 01 laboratory 07<--")

    url = 'http://sdi.gdos.gov.pl/wfs'
    v = '1.1.0'
    layer = 'GDOS:ParkiNarodowe'

    wfs = get_data(url, 1, v)
    _, ds_name = get_layer(wfs, layer)

    drawa = PropertyIsEqualTo(propertyname='kodinspire', literal='PL.ZIPOP.1393.PN.18')
    wolin = PropertyIsEqualTo(propertyname='kodinspire', literal='PL.ZIPOP.1393.PN.4')
    xml = etree.tostring(Or([drawa, wolin]).toXML()).decode("utf-8")

    data = str(wfs.getfeature(typename=layer, filter=xml).read(), 'utf-8')

    try:
        out = open(os.path.join(export_folder, 'data.gml'), 'wb')
        out.write(bytes(data, 'utf-8'))
        out.close()
    except IOError:
        print("Data folder not found! Restart the script!")
        os.mkdir(export_folder)

    src = os.path.abspath(os.path.join(export_folder, 'data.gml'))
    dst = os.path.abspath(export_folder)
    dst_crs = 'EPSG:2180'

    subprocess.call(f"ogr2ogr -t_srs {dst_crs} '{dst}/{ds_name}.gpkg' '{src}'", shell=True)
    subprocess.call(f"ogr2ogr -t_srs {dst_crs} '{dst}/{ds_name}.csv' '{src}' -lco GEOMETRY=AS_WKT", shell=True)

    print("-->Ended exercise 01 laboratory 07<--")
