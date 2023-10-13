import click
from espa import Metadata


@click.command()
@click.argument(
    "inputxmlfile",
    type=click.Path(dir_okay=False, file_okay=True,),
)
@click.argument(
    "outputxmlfile",
    type=click.Path(),
)
@click.argument(
    "hdffile",
    type=click.Choice(["one", "two"], case_sensitive=True,),
)
def main(inputxmlfile, outputxmlfile, hdffile):
    mm = Metadata(xml_filename=inputxmlfile)
    mm.parse()
    hls_product = 'hls'
    if hdffile == 'one':
        for band in mm.xml_object.bands.iterchildren():
            if band.get('name') == 'sr_band1':
                band.set('name', 'band01')
                band.set('product', hls_product)
            elif band.get('name') == 'sr_band2':
                band.set('name', 'blue')
                band.set('product', hls_product)
            elif band.get('name') == 'sr_band3':
                band.set('name', 'green')
                band.set('product', hls_product)
            elif band.get('name') == 'sr_band4':
                band.set('name', 'red')
                band.set('product', hls_product)
            elif band.get('name') == 'sr_band5':
                band.set('name', 'band05')
                band.set('product', hls_product)
            elif band.get('name') == 'sr_band6':
                band.set('name', 'band06')
                band.set('product', hls_product)
            elif band.get('name') == 'sr_band7':
                band.set('name', 'band07')
                band.set('product', hls_product)
            elif band.get('name') == 'sr_band8':
                band.set('name', 'band08')
                band.set('product', hls_product)
    elif hdffile == 'two':
        for band in mm.xml_object.bands.iterchildren():
            if band.get('name') == 'sr_band8a':
                band.set('name', 'band8a')
                band.set('product', hls_product)
            elif band.get('name') == 'sr_band9':
                band.set('name', 'band09')
                band.set('product', hls_product)
            elif band.get('name') == 'sr_band10':
                band.set('name', 'band10')
                band.set('product', hls_product)
            elif band.get('name') == 'sr_band11':
                band.set('name', 'band11')
                band.set('product', hls_product)
            elif band.get('name') == 'sr_band12':
                band.set('name', 'band12')
                band.set('product', hls_product)
            elif band.get('name') == 'sr_aerosol_qa':
                band.set('name', 'CLOUD')
                band.set('product', hls_product)

    for band in mm.xml_object.bands.iterchildren():
        if band.get('product') != hls_product:
            print((band.get('name')))
            mm.xml_object.bands.remove(band)

    mm.write(xml_filename=outputxmlfile)


if __name__ == "__main__":
    main()
