import os
import glob
import click


@click.command()
@click.argument(
    "inputs2dir",
    type=click.Path(dir_okay=True, file_okay=False,),
)
def main(inputs2dir):
    extension = None
    # determine the name of the {product_id} directory under GRANULE
    granule_dir = os.path.join(inputs2dir, 'GRANULE')

    # check if it is an old format SAFE directory
    gml_path = glob.glob("{}/*/QI_DATA/DETFOO_B06.gml".format(granule_dir))
    if len(gml_path) > 0:
        extension = "gml"

    jp2_path = glob.glob("{}/*/QI_DATA/DETFOO_B06.jp2".format(granule_dir))
    if len(jp2_path) > 0:
        extension = "jp2"

    if extension is None:
        raise FileNotFoundError

    click.echo(extension)


if __name__ == "__main__":
    main()
