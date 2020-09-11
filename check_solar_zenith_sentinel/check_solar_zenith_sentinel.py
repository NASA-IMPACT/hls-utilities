from lxml import etree
import click


@click.command()
@click.argument(
    "inputxml",
    type=click.Path(dir_okay=False, file_okay=True,),
)
def main(inputxml):
    """check_solar_zenith_sentinel MTD_TL.xml"""
    doc = etree.parse(inputxml)
    element = doc.xpath("//Mean_Sun_Angle/ZENITH_ANGLE")[0]
    solar_zenith = float(element.text)
    if (solar_zenith > 76):
        click.echo("invalid")
    else:
        click.echo("valid")


if __name__ == "__main__":
    main()
