from setuptools import setup, find_packages

setup(
    name="hls-utilities",
    version="1.11.3",
    packages=find_packages(),
    install_requires=[
        "click",
        "lxml",
        "boto3",
        "espa-python-library @ git+https://github.com/USGS-EROS/espa-python-library.git@v2.0.0#egg=espa-python-library",
        "rasterio",
        "numpy",
    ],
    include_package_data=True,
    extras_require={
        "dev": ["ruff"],
        "test": ["ruff", "pytest", "Jinja2", "moto[s3]", "markupsafe==2"]
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
