import click
from .mtlutils import parsemeta


@click.command()
@click.argument(
    "inputmtl",
    type=click.Path(dir_okay=False, file_okay=True,),
)
def main(inputmtl):
    """check_solar_zenith_landsat _MTL.txt"""
    metadata = parsemeta(inputmtl)
    try:
        sun_elevation = float(
            metadata["L1_METADATA_FILE"]["IMAGE_ATTRIBUTES"]["SUN_ELEVATION"]
        )
    except KeyError:
        sun_elevation = float(
            metadata["LANDSAT_METADATA_FILE"]["IMAGE_ATTRIBUTES"]["SUN_ELEVATION"]
        )

    solar_zenith = 90 - sun_elevation
    if (solar_zenith > 76):
        click.echo("invalid")
    else:
        click.echo("valid")


if __name__ == "__main__":
    main()
