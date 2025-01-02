from typing import List, Optional, Tuple
from pathlib import Path

import click
import rasterio


# MSI band number definitions for bands used by HLS v2 product
# (coastal, blue/green/red, NIR, SWIR1, SWIR2)
SPECTRAL_BANDS = frozenset({
    "B01",
    "B02",
    "B03",
    "B04",
    "B8A",
    "B11",
    "B12",
})


def _one_or_none(paths: List[Path]) -> Optional[Path]:
    if len(paths) == 1:
        return paths[0]


def find_image_mask_pairs(granule_dir: Path) -> List[Tuple[Path, Path]]:
    """Search granule directory for image + mask pairs

    The quality masks were produced in an imagery format since baseline 04.00
    (~Jan 25, 2022 and onward), so this function might return nothing
    if run on granules created with older baselines. These older baselines
    encoded the mask quality information in the GML (vector) format.

    The relevant parts of an unzipped granule looks like,
    ```
    ${GRANULE_ID}.SAFE
    ${GRANULE_ID}.SAFE/GRANULE
    ${GRANULE_ID}.SAFE/GRANULE/L1C_T45TXF_A038726_20221121T050115
    ${GRANULE_ID}.SAFE/GRANULE/L1C_T45TXF_A038726_20221121T050115/IMG_DATA
    ${GRANULE_ID}.SAFE/GRANULE/L1C_T45TXF_A038726_20221121T050115/IMG_DATA/T45TXF_20221121T050121_B01.jp2
    ... (*B*.jp2)
    ${GRANULE_ID}.SAFE/GRANULE/L1C_T45TXF_A038726_20221121T050115/QI_DATA
    ${GRANULE_ID}.SAFE/GRANULE/L1C_T45TXF_A038726_20221121T050115/QI_DATA/MSK_QUALIT_B01.jp2
    ... (MSK_QUALIT_B*.jp2)
    ```

    References
    ----------
    https://sentinels.copernicus.eu/web/sentinel/-/copernicus-sentinel-2-major-products-upgrade-upcoming
    """
    pairs = []
    for band in SPECTRAL_BANDS:
        image = _one_or_none(list(granule_dir.glob(f"**/IMG_DATA/*{band}.jp2")))
        mask = _one_or_none(list(granule_dir.glob(f"**/QI_DATA/MSK_QUALIT_{band}.jp2")))
        if image and mask:
            pairs.append((image, mask))

    # Find all bands, or none
    if len(pairs) == len(SPECTRAL_BANDS):
        return pairs
    return []


def apply_quality_mask(image: Path, mask: Path):
    """Apply Sentinel-2 image quality mask

    Each spectral band (`IMG_DATA/B*.jp2`) has a corresponding quality mask
    image (`QI_DATA/MSK_QUALIT_B*.jp2`) of the same spatial resolution. The mask
    image has 8 bands, with each band encoding a boolean for the presence/absence
    of a quality issue. The bands indicate,

    1: lost ancillary packets
    2: degraded ancillary packets
    3: lost MSI packets
    4: degraded MSI packets
    5: defective pixels
    6: no data
    7: partially corrected cross talk
    8: saturated pixels

    We have decided to mask 3 (lost MSI packets) and 4 (degraded MSI packets) only.
    So far, 5 and 7 are present in  B10-B11, because interpolation is used to fill 5
    and the cross talk is partially corrected.
    Saturated pixels are still useful for the magnitude of the reflectance; keep it.

    We apply the mask by updating the spectral data images in-place rather than
    creating another file.

    References
    ----------
    https://sentinels.copernicus.eu/web/sentinel/technical-guides/sentinel-2-msi/data-quality-reports
    """
    with rasterio.open(mask) as mask_src:
        qa_bands = mask_src.read(indexes=[3, 4])
        lost_degraded_mask = (qa_bands == 1).any(axis=0)

    # only update imagery if mask shows it has any bad pixels
    if lost_degraded_mask.any():
        click.echo(f"Masking lost or degraded pixel values in {image}")
        with rasterio.open(image, "r+") as img_src:
            img = img_src.read(1)
            # L1C images don't define the nodata value on file so we can't update the
            # mask (e.g., via `write_mask`) but 0 is used as the nodata value
            # (see SPECIAL_VALUE_INDEX for NODATA in metadata)
            img[lost_degraded_mask] = 0
            img_src.write(img, indexes=1)


@click.command()
@click.argument(
    "granule_dir",
    type=click.Path(file_okay=False, dir_okay=True, exists=True),
)
def main(granule_dir: Path):
    """Update Sentinel-2 imagery by masking lost or degraded pixels"""
    granule_dir = Path(granule_dir)
    click.echo(f"Applying Sentinel-2 QAQC mask to granule_dir={granule_dir}")

    image_mask_pairs = find_image_mask_pairs(granule_dir)

    for (image, mask) in image_mask_pairs:
        apply_quality_mask(image, mask)

    click.echo("Complete")


if __name__ == "__main__":
    main()
