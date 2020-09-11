from click.testing import CliRunner
from parse_fmask.parse_fmask import main


def test_parse_fmask_invalid():
    fmaskoutput = \
        """Fmask 4.2 start ...
        Cloud/cloud shadow/snow dilated by 3/3/0 pixels.
        probability threshold of 20.00%.
        or calculate TOA reflectances.
        potential clouds, cloud shadows, snow, and water.
        clear pixel in this image (clear-sky pixels = 102Fmask 4.2 finished (3.95 minutes)
        for L1C_T37WFN_A017436_20200708T084600 with 0.00% clear pixels
        Input file size is 5490, 5490
        0...10...20...30...40...50...60...70...80...90...100 - done."""

    runner = CliRunner(echo_stdin=True)
    result = runner.invoke(main, [
        fmaskoutput
    ], catch_exceptions=False)
    assert result.exit_code == 0
    assert result.stdout == "invalid\n"


def test_parse_fmask_valid():
    fmaskoutput = \
        """Fmask 4.2 start ...
        Cloud/cloud shadow/snow dilated by 3/3/0 pixels.
        probability threshold of 20.00%.
        or calculate TOA reflectances.
        potential clouds, cloud shadows, snow, and water.
        clear pixel in this image (clear-sky pixels = 102Fmask 4.2 finished (3.95 minutes)
        for L1C_T37WFN_A017436_20200708T084600 with 0.00% clear pixels
        Input file size is 5490, 5490
        0...10...20...30...40...50...60...70...80...90...100 - done."""

    runner = CliRunner(echo_stdin=True)
    result = runner.invoke(main, [
        fmaskoutput
    ], catch_exceptions=False)
    assert result.exit_code == 0
    assert result.stdout == "invalid\n"
