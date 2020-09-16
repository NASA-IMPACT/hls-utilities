import os
import lxml
from click.testing import CliRunner
from create_sr_hdf_xml.create_sr_hdf_xml import main


current_dir = os.path.dirname(__file__)
test_dir = os.path.join(current_dir, "data")


def test_create_sr_hdf_xml_one(tmpdir):
    inputxml = os.path.join(test_dir,
                            "S2A_MSI_L1C_T17RKP_20200426_20200426.xml")
    # Unfortunate espa tmp prefixing only allows running in current dir.
    os.chdir(tmpdir.strpath)
    outputxmlfile = "outputxmlfile_1.xml"
    hdffile = "one"

    runner = CliRunner(echo_stdin=True)
    result = runner.invoke(main, [
        inputxml,
        outputxmlfile,
        hdffile
    ], catch_exceptions=False)
    tree = lxml.etree.parse(outputxmlfile)
    root = tree.getroot()
    count = len(root[1])
    assert count == 8
    assert result.exit_code == 0


def test_create_sr_hdf_xml_two(tmpdir):
    inputxml = os.path.join(test_dir,
                            "S2A_MSI_L1C_T17RKP_20200426_20200426.xml")
    # Unfortunate espa tmp prefixing only allows running in current dir.
    os.chdir(tmpdir.strpath)
    outputxmlfile = "outputxmlfile_1.xml"
    hdffile = "two"

    runner = CliRunner(echo_stdin=True)
    result = runner.invoke(main, [
        inputxml,
        outputxmlfile,
        hdffile
    ], catch_exceptions=False)
    tree = lxml.etree.parse(outputxmlfile)
    root = tree.getroot()
    count = len(root[1])
    assert count == 6
    assert result.exit_code == 0
