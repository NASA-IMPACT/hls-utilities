from pathlib import Path
from typing import Tuple

import numpy as np
import pytest
import rasterio
from affine import Affine
from rasterio.crs import CRS

from apply_s2_quality_mask.apply_s2_quality_mask import (
    JPEG2000_NO_COMPRESSION_OPTIONS,
    SPECTRAL_BANDS,
    apply_quality_mask,
    find_image_mask_pairs,
)


def make_fake_s2_granule(
    prefix: Path,
    band: str,
    mask_data: np.ndarray,
) -> Tuple[Path, Path]:
    """Create a fake S2 L1C granule"""

    profile = {
        "width": mask_data.shape[1],
        "height": mask_data.shape[2],
        "crs": CRS.from_epsg(32643),
        "transform": Affine(10.0, 0.0, 399960.0, 0.0, -10.0, 2700000.0),
        "driver": "JP2OpenJPEG",
        **JPEG2000_NO_COMPRESSION_OPTIONS,
    }

    image_path = prefix / "IMG_DATA" / f"T45TXF_20221121T050121_{band}.jp2"
    image_path.parent.mkdir(exist_ok=True, parents=True)
    with rasterio.open(image_path, "w", count=1, dtype="uint16", **profile) as dst:
        dst.write(np.ones(mask_data.shape[1:]), 1)

    mask_path = prefix / "QI_DATA" / f"MSK_QUALIT_{band}.jp2"
    mask_path.parent.mkdir(exist_ok=True, parents=True)
    with rasterio.open(mask_path, "w", count=8, dtype="uint8", **profile) as dst:
        dst.write(mask_data)

    return image_path, mask_path


def test_find_image_mask_pairs_found_all(tmp_path: Path):
    """Test successfully finding location of all imagery data"""
    granule_id = "L1C_T45TXF_A038726_20221121T050115"
    granule_prefix = tmp_path / f"{granule_id}.SAFE" / "GRANULE" / granule_id

    mask_data = np.zeros((8, 1, 1), dtype="uint8")

    expected_images_masks = []
    for band in SPECTRAL_BANDS:
        expected_images_masks.append(make_fake_s2_granule(granule_prefix, band, mask_data))

    # Make sure we find all of the expected paths
    image_mask_pairs = find_image_mask_pairs(tmp_path)

    for image_mask_pair in expected_images_masks:
        assert image_mask_pair in image_mask_pairs


def test_find_image_mask_pairs_found_not_all(tmp_path: Path):
    """Test this is a no-op if we can't find all of the mask<>image pairs"""
    granule_id = "L1C_T45TXF_A038726_20221121T050115"
    granule_prefix = tmp_path / f"{granule_id}.SAFE" / "GRANULE" / granule_id

    mask_data = np.zeros((8, 1, 1), dtype="uint8")

    expected_images_masks = []
    for band in list(SPECTRAL_BANDS)[:2]:
        expected_images_masks.append(make_fake_s2_granule(granule_prefix, band, mask_data))

    # Make sure we find all of the expected paths
    image_mask_pairs = find_image_mask_pairs(tmp_path)
    assert not image_mask_pairs


def test_apply_quality_mask_overwrites_value(tmp_path: Path):
    """Ensure image data are set to no data value (0) per mask band"""
    # Mask is 2x2 with 4 test cases,
    #   * (0, 0) ~> unmasked
    #   * (0, 1) ~> lost MSI packet
    #   * (1, 0) ~> degraded MSI packet
    #   * (1, 1) ~> lost + degraded MSI packet (both set)
    mask_data = np.zeros((8, 2, 2), dtype="uint8")
    mask_data[2, 0, 1] = 1
    mask_data[3, 1, 0] = 1
    mask_data[2, 1, 1] = 1
    mask_data[3, 1, 1] = 1
    assert mask_data.sum() == 4

    granule_id = "L1C_T45TXF_A038726_20221121T050115"
    granule_prefix = tmp_path / f"{granule_id}.SAFE" / "GRANULE" / granule_id

    image, mask = make_fake_s2_granule(granule_prefix, "B02", mask_data)

    apply_quality_mask(image, mask)

    # Check data ~> image should have 0s in 3 pixel locations
    with rasterio.open(image) as src:
        image_data = src.read(1)

    np.testing.assert_array_equal(
        image_data,
        np.array([[1, 0], [0, 0]], dtype="uint16"),
    )
