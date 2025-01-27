from setuptools import setup, find_packages

setup(
    name="hls-utilities",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "click~=7.1.0",
        "lxml",
        "boto3~=1.17.91",
        "espa-python-library @ git+https://github.com/USGS-EROS/espa-python-library.git@v2.0.0#egg=espa-python-library",
        "rasterio~=1.2",
        "numpy~=1.16",
    ],
    include_package_data=True,
    extras_require={
        "dev": ["flake8", "black"],
        "test": ["flake8", "pytest", "Jinja2==2.10.1", "moto[s3]~=2.0.8"]
    },
    entry_points={"console_scripts": [
        "apply_s2_quality_mask=apply_s2_quality_mask.apply_s2_quality_mask:main",
        "parse_fmask=parse_fmask.parse_fmask:main",
        "check_solar_zenith_sentinel=check_solar_zenith_sentinel.check_solar_zenith_sentinel:main",
        "check_solar_zenith_landsat=check_solar_zenith_landsat.check_solar_zenith_landsat:main",
        "get_s2_granule_dir=get_s2_granule_dir.get_s2_granule_dir:main",
        "get_doy=get_doy.get_doy:main",
        "create_sr_hdf_xml=create_sr_hdf_xml.create_sr_hdf_xml:main",
        "create_landsat_sr_hdf_xml=create_landsat_sr_hdf_xml.create_landsat_sr_hdf_xml:main",
        "check_sentinel_clouds=check_sentinel_clouds.check_sentinel_clouds:main",
        "download_landsat=download_landsat.download_landsat:main",
        "get_detector_footprint=get_detector_footprint.get_detector_footprint:main",
        "get_detector_footprint_extension=get_detector_footprint_extension.get_detector_footprint_extension:main",
    ]},
)
