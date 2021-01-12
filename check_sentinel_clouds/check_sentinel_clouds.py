from lxml import etree
import click


@click.command()
@click.argument(
    "inputxml",
    type=click.Path(dir_okay=False, file_okay=True,),
)
def main(inputxml):
    """check_sentinel_clouds MTD_MSIL1C.xml"""
    doc = etree.parse(inputxml)
    element = doc.xpath("//Cloud_Coverage_Assessment")[0]
    cloud = float(element.text)
    if (cloud > 95):
        click.echo("invalid")
    else:
        click.echo("valid")


if __name__ == "__main__":
    main()
