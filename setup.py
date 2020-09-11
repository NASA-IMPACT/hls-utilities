from setuptools import setup, find_packages

setup(
    name="hls-utilities",
    version="0.1",
    packages=find_packages(),
    install_requires=["click", ],
    include_package_data=True,
    extras_require={"dev": ["flake8", "black"], "test": ["flake8", "pytest"]},
    entry_points={"console_scripts": ["parse_fmask=parse_fmask.parse_fmask:main", ]},
)
