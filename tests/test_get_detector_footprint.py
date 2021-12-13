import os
from click.testing import CliRunner
from get_detector_footprint.get_detector_footprint import main


current_dir = os.path.dirname(__file__)
test_dir = os.path.join(current_dir, "data")


def test_get_detector_footprint():
    runner = CliRunner(echo_stdin=True)
    inputs2dir = os.path.join(
        test_dir,
        "S2A_MSIL1C_20210708T184921_N0301_R113_T11VNF_20210708T222235.SAFE",
    )
    expected = os.path.join(
        test_dir,
        "S2A_MSIL1C_20210708T184921_N0301_R113_T11VNF_20210708T222235.SAFE/"
        "GRANULE/L1C_T11VNF_A031570_20210708T185756/QI_DATA/DETFOO_B06.gml\n",
    )
    result = runner.invoke(main, [
        inputs2dir
    ], catch_exceptions=False)
    assert result.stdout == expected

    inputs2dir = os.path.join(
        test_dir,
        "S2A_MSIL1C_20210708T184921_N0301_R113_T11VNF_20210708T222236.SAFE",
    )
    expected = os.path.join(
        test_dir,
        "S2A_MSIL1C_20210708T184921_N0301_R113_T11VNF_20210708T222236.SAFE/"
        "GRANULE/L1C_T11VNF_A031570_20210708T185756/QI_DATA/DETFOO_B06.jp2\n",
    )
    result = runner.invoke(main, [
        inputs2dir
    ], catch_exceptions=False)
    assert result.stdout == expected
