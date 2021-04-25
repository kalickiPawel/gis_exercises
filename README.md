# Geoinformatics personal training repo

## Prepared:

### Laboratory 7:
#### 1. Exercise
   
- write script to download data from WFS:
[WGS - Generalnej Dyrekcji Ochrony Środowiska](https://sdi.gdos.gov.pl/wfs)
- with CRS: EPSG:2180
- filter the data in order to obtain ParkiNarodowe layer
- get data only for Wolin and Drawa National Parks
- save data to geopackage file and table 'parki_narodowe'

#### 2. Exercise

- write script to download data from specific WMS service with specific bounding box.
- allows selecting layer, raster format and resolution
- download informations with getfeatureinfo from center of tile

#### 3. Exercise

- write script to download tiles from WMS service with specific bounding box and resolution.
- merge tiles using the GDAL library and save as geotiff file
