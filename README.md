# hls-utilities
## Python utilities for HLS data processing containers

## Usage
```bash
$ apply_s2_quality_mask INPUTS2DIR
```
```bash
$ check_solar_zenith_sentinel INPUTXML
```
```bash
$ check_solar_zenith_landsat INPUTXML
```
```bash
$ create_sr_hdf_xml INPUTXMLFILE OUTPUTXMLFILE [one|two]
```
```bash
$ create_landsat_sr_hdf_xml INPUTXMLFILE OUTPUTXMLFILE
```
```bash
$ get_doy YEAR MONTH DAY
```
```bash
$ get_s2_granule_dir INPUTS2DIR
```
```bash
$ parse_fmask FMASKOUTPUT
```
```bash
$ download_landsat BUCKET PATH OUTPUT_DIRECTORY  
```
```bash
$ get_detector_footprint INPUTS2DIR
```
```bash
$ get_detector_footprint_extension INPUTS2DIR
```


### Tests
Run Tests
```bash
$ tox
```
