#!/usr/bin/env python
"""Create a KML file from a geotiff and a png"""

from __future__ import print_function, absolute_import, division, unicode_literals

import argparse
import os
import sys
import lxml.etree as et
from osgeo import gdal
import zipfile


def makeKML(geotiff,pngFile):

    # Extract information from GeoTIFF
    raster = gdal.Open(geotiff)

    # Extract metadata from GeoTIFF to fill into the KML
    gt = raster.GetGeoTransform()
    coordStr = ('%.4f,%.4f %.4f,%.4f %.4f,%.4f %.4f,%.4f' %
      (gt[0], gt[3]+raster.RasterYSize*gt[5], gt[0]+raster.RasterXSize*gt[1],
        gt[3]+raster.RasterYSize*gt[5], gt[0]+raster.RasterXSize*gt[1], gt[3],
        gt[0], gt[3]))

    # Take care of namespaces
    prefix = {}
    gx = '{http://www.google.com/kml/ext/2.2}'
    prefix['gx'] = gx
    ns_gx = {'gx' : 'http://www.google.com/kml/ext/2.2'}
    ns_main = { None : 'http://www.opengis.net/kml/2.2'}
    ns = dict(list(ns_main.items()) + list(ns_gx.items()))

    # Fill in the tree structure
    kmlFile = pngFile.replace('.png','.kml')
    kml = et.Element('kml', nsmap=ns)
    overlay = et.SubElement(kml, 'GroundOverlay')
    et.SubElement(overlay, 'name').text = \
      os.path.basename(kmlFile).replace('.kml', '') + ' overlay'
    icon = et.SubElement(overlay, 'Icon')
    et.SubElement(icon, 'href').text = pngFile
    et.SubElement(icon, 'viewBoundScale').text = '0.75'
    latLonQuad = et.SubElement(overlay, '{0}LatLonQuad'.format(gx))
    et.SubElement(latLonQuad, 'coordinates').text = coordStr
    with open(kmlFile, 'w') as outF:
      outF.write(et.tostring(kml, xml_declaration=True, encoding='utf-8',
        pretty_print=True))
    outF.close()

    # Zip PNG and KML together
    zipFile = kmlFile.replace('.kml', '.kmz')
    zip = zipfile.ZipFile(zipFile, 'w', zipfile.ZIP_DEFLATED)
    zip.write(kmlFile)
    zip.write(pngFile)
    zip.close()


def main():
    """Main entrypoint"""

    # entrypoint name can differ from module name, so don't pass 0-arg
    cli_args = sys.argv[1:] if len(sys.argv) > 1 else None

    parser = argparse.ArgumentParser(
        prog=os.path.basename(__file__),
        description=__doc__,
    )
    parser.add_argument('geotiff', help='name of GeoTIFF file (input)')
    parser.add_argument('pngFile', help='name of PNG file (input)')
    args = parser.parse_args(cli_args)

    if not os.path.exists(args.geotiff):
        print('GeoTIFF file (%s) does not exist!' % args.geotiff)
        sys.exit(1)
    if not os.path.exists(args.pngFile):
        print('PNG file (%s) does not exist!' % args.pngFile)
        sys.exit(1)

    makeKML(args.geotiff, args.pngFile)


if __name__ == '__main__':
    main()
