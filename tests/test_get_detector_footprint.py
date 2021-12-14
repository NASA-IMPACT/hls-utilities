import os
import pytest
from click.testing import CliRunner
from get_detector_footprint.get_detector_footprint import main


safedirectory = "S2A_MSIL1C_20210708T184921_N0301_R113_T11VNF_20210708T222235.SAFE"


def test_get_detector_footprint_gml(tmpdir):
    runner = CliRunner(echo_stdin=True)
    safe_path = os.path.join(tmpdir, safedirectory)
    fake_safe = tmpdir.mkdir(safedirectory).mkdir("GRANULE") \
        .mkdir("L1C_T11VNF_A031570_20210708T185756").mkdir("QI_DATA")
    fake_detfoo = fake_safe.join("MSK_DETFOO_B06.gml")
    fake_detfoo.write("content")
    result = runner.invoke(main, [safe_path], catch_exceptions=False)
    assert result.stdout == fake_detfoo + "\n"


def test_get_detector_footprint_jp2(tmpdir):
    runner = CliRunner(echo_stdin=True)
    safe_path = os.path.join(tmpdir, safedirectory)
    fake_safe = tmpdir.mkdir(safedirectory).mkdir("GRANULE") \
        .mkdir("L1C_T11VNF_A031570_20210708T185756").mkdir("QI_DATA")
    fake_detfoo = fake_safe.join("MSK_DETFOO_B06.jp2")
    fake_detfoo.write("content")
    result = runner.invoke(main, [safe_path], catch_exceptions=False)
    assert result.stdout == fake_detfoo + "\n"


def test_get_detector_footprint_invalid(tmpdir):
    runner = CliRunner(echo_stdin=True)
    safe_path = os.path.join(tmpdir, safedirectory)

    with pytest.raises(FileNotFoundError):
        runner.invoke(main, [safe_path], catch_exceptions=False)
