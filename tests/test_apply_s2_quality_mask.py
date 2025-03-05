from pathlib import Path
from typing import List, Tuple

import numpy as np
import pytest
import rasterio
from affine import Affine
from rasterio.crs import CRS

from apply_s2_quality_mask.apply_s2_quality_mask import (
    JPEG2000_NO_COMPRESSION_OPTIONS,
    SPECTRAL_BANDS,
    apply_quality_mask,
    build_quality_mask,
    find_affected_bands,
    find_image_mask_pairs,
)

TEST_DATA = Path(__file__).parents[0].joinpath("data", "quality-mask")


@pytest.mark.parametrize(["granule_dir", "affected_bands"], [
    pytest.param(
        TEST_DATA / "L1C_T45TXF_A038726_20221121T050115",
        ["B01", "B02", "B03", "B04", "B05", "B06", "B07", "B08", "B09", "B10", "B11", "B12", "B8A"],
        id="All bands affected",
    ),
    pytest.param(
        TEST_DATA / "L1C_T43QDG_A031305_20230305T053523",
        ["B01", "B02", "B03", "B09", "B10", "B11", "B12", "B8A"],
        id="Subset of bands affected",
    ),
    pytest.param(
        TEST_DATA / "L1C_T12QXM_A048143_20240909T175112",
        [],
        id="No bands affected",
    ),
    pytest.param(
        TEST_DATA,
        SPECTRAL_BANDS,
        id="No metadata file present",
    )
])
def test_find_affected_bands(granule_dir: Path, affected_bands: List[str]):
    """Test we find the bands affected by a quality issue correctly from metadata"""
    test = find_affected_bands(granule_dir)
    assert set(test) == set(affected_bands)


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

    expected_images_masks = {}
    for band in SPECTRAL_BANDS:
        expected_images_masks[band] = make_fake_s2_granule(granule_prefix, band, mask_data)

    # Make sure we find all of the expected paths
    image_mask_pairs = find_image_mask_pairs(tmp_path, SPECTRAL_BANDS)

    for band, expected_images_masks in expected_images_masks.items():
        assert image_mask_pairs[band] == expected_images_masks


def test_find_image_mask_pairs_found_not_all(tmp_path: Path):
    """Test this is a no-op if we can't find all of the mask<>image pairs"""
    granule_id = "L1C_T45TXF_A038726_20221121T050115"
    granule_prefix = tmp_path / f"{granule_id}.SAFE" / "GRANULE" / granule_id

    mask_data = np.zeros((8, 1, 1), dtype="uint8")

    expected_images_masks = []
    for band in list(SPECTRAL_BANDS)[:2]:
        expected_images_masks.append(make_fake_s2_granule(granule_prefix, band, mask_data))

    # Make sure we find all of the expected paths
    image_mask_pairs = find_image_mask_pairs(tmp_path, SPECTRAL_BANDS)
    assert not image_mask_pairs


def test_apply_quality_mask_overwrites_value(tmp_path: Path):
    """Ensure image data are set to no data value (0) per mask band"""
    # Mask is 2x2 with 4 test cases,
    #   * (0, 0) ~> unmasked
    #   * (0, 1) ~> lost MSI packet
    #   * (1, 0) ~> degraded MSI packet
    #   * (1, 1) ~> lost + degraded MSI packet (both set)
    qa_data = np.zeros((8, 2, 2), dtype="uint8")
    qa_data[2, 0, 1] = 1
    qa_data[3, 1, 0] = 1
    qa_data[2, 1, 1] = 1
    qa_data[3, 1, 1] = 1
    assert qa_data.sum() == 4

    granule_id = "L1C_T45TXF_A038726_20221121T050115"
    granule_prefix = tmp_path / f"{granule_id}.SAFE" / "GRANULE" / granule_id

    image_path, qa_image_path = make_fake_s2_granule(granule_prefix, "B02", qa_data)

    mask = build_quality_mask([qa_image_path])
    apply_quality_mask(image_path, mask)

    # Check data ~> image should have 0s in 3 pixel locations
    with rasterio.open(image_path) as src:
        image_data = src.read(1)

    np.testing.assert_array_equal(
        image_data,
        np.array([[1, 0], [0, 0]], dtype="uint16"),
    )
