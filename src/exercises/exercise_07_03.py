from src.get_from_wms_or_wfs import get_data, get_map, get_tiles


def run(export_folder):
    print("-->Started exercise 03 laboratory 07<--")

    box = '299000,446000,299100,446100'
    filename = 'zad03'
    num_of_tiles = 4
    tile = 200

    wms = get_data('https://mapy.geoportal.gov.pl/wss/service/PZGIK/ORTO/WMS/StandardResolution', 0, '1.3.0')
    get_tiles(wms, num_of_tiles, tile, box, export_folder, filename)

    print("-->Ended exercise 03 laboratory 07<--")
