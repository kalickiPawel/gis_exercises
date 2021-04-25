from src.get_from_wms_or_wfs import get_data, get_map, get_center_tile


def run(export_folder):
    print("-->Started exercise 02 laboratory 07<--")

    url = 'https://integracja.gugik.gov.pl/cgi-bin/KrajowaIntegracjaEwidencjiGruntow'
    version = '1.3.0'

    wms = get_data(url, 0, version)

    layer = 'powiaty'
    bbox = '192695,571489,309663,692294'

    raster_ext = "png"
    raster = {
        'size': (500, 500),
        'format': "image/" + raster_ext,
        'extension': raster_ext
    }

    resp_map = get_map(wms, layer, raster, bbox, export_folder)
    resp_gfi = get_center_tile(wms, layer, raster, bbox, export_folder)

    print(f"Response for GetMap: {resp_map}")
    print(f"Response for GetFeatureInfo: {resp_gfi}")

    print("-->Ended exercise 02 laboratory 07<--")
