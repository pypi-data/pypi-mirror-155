## General Description

- Purpose: Retrieve CMEMS sea-surface height forecasts at the coast (EU-wide) and add other relevant processes to produce a coastal total water-level TWL, and evaluate the TWLs against pre-defined flood-triggering thresholds.
- Outputs: 
  -Netcdf files based on the bulleting date of the execution day (t0) containing coastal time-series for the selected product-region (ARC,MED,IBI,BS,BAL,NWS) for 7 days [t0-2 : t0+5] (dimensions Ncoastalpoints x times) 
  -a csv file containing the triggering information for each coastal point as defined by the pre-defined target coastal points (e.g. the hindcast in the case of ECFAS). 

## Installation

We recommend using [miniconda](https://docs.conda.io/en/latest/miniconda.html).

### Create an 'ecfas' virtual environment and install conda dependencies

```
$ conda create -n 'ecfas' python'>3.8,<3.9' libnetcdf==4.7.3
$ conda activate ecfas
$ conda install -y -c fbriol pyfes==2.9.2
$ conda install -y -c conda-forge proj==7.2.0
$ conda install -y xarray==0.16
$ conda install -y geos==3.8.1
```

### Option 1: PIP (current stable release)

```
$ pip install ecfas
```

### Option 2: Git-Clone and install from sources (current master-branch version)
This option is ideal if you want to edit the code. Clone the repository:

```
$ git clone git@gitlab.mercator-ocean.fr:mirazoki/ecfas.git
```
Change into its directory and install it:

```
$ cd ecfas
$ pip install -e .
```
You are now ready to go

### External dependencies

- **Note: Location of the external files needs to be specified in the configuration file**

- Summer masks need to be downloaded from https://nexus.mercator-ocean.fr/repository/moistatics/ECFAS/masks.tar.gz.

- This implementation also requires [FES2014](https://www.aviso.altimetry.fr/fr/donnees/produits/produits-auxiliaires/maree-oceanique-fes.html) tide data from AVISO. You will need to [register](https://www.aviso.altimetry.fr/en/data/data-access/registration-form.html) for an account, download the data from the [AVISO ftp site](ftp://ftp-access.aviso.altimetry.fr/auxiliary/tide_model/fes2014_elevations_and_load).


### Create a configuration file

Create a file with the following content:

```
# CMEMS credentials and url for data donload
usr=
pwd=
url=http://nrt.cmems-du.eu/motu-web/Motu
# Directory for outputs
outdir=
# Directory for masks
maskdir=
# Leave blank if do not want any log files (console output only)
logdir=
# FES data, if blank then there is none
fesdir=
```
Directories paths can be absolute or relative. If relative, they will assumed to be relative to the scripts' running directory. 

## Usage
The package currently comprises two commands:
-op_workflow: function that generates the coastal TWL netcdf series based on the CMEMS products.
-op_trigger: function that evaluates the TWLs generated in op_workflow againt pre-defined target coastal points and their correponding thresholds for triggering and extreme event duration determination. The output is a csv file with the trigger information, defined on the target coastal points

For ECFAS, the commands should be run sequentially, first the workflow and then the trigger. The workflow can be run independently (and hence in parallel) for each regional domain, while the trigger should be run once the workflow has run for all domains.  A description of how to run each of the commands is provided below. 

### Running the workflow (op_workflow)
- User guide: The workflow is run separately for each regional domain in Europe, namely NWS,IBI,MED,BAL,BS,ARC (see optional argument -r)
For operational purposes (e.g. ECFAS), the workflow should be scheduled at the corresponding daily forecast update time for each domain:

  
  - NWS: North West Shelf, daily update time:  12:00

  - IBI: Iberian Biscay and Ireland , daily update time:  14:00

  - MED: Mediterranean Sea , daily update time:  20:00

  - BAL: Baltic Sea , daily update time:  22:00

  - BS: Black Sea , daily update time:  12:00
  - ARC: Arctic , daily update time:  04:00

The workflow needs as a minimum the configuration file to run. The optional arguments are the following:

    -r <region> : Region, matching the 6 Copernicus Marine Service regional domains (see User guide). Default: NWS

    -t <%Y%m%d_%H%M%S>: Bulleting date for the forecast data. Default: Forecast update time of execution day

- Usage: `op_workflow -c <config_file> [-r <region>] [-t <%Y%m%d_%H%M%S>] [--reanal] [--debug]`

Example call: `op_workflow -c ecfas.cnf -r NWS -t 20220125_000000`

The debug flag will notably prevent cleaning up of previously downloaded files (which is the default) in
order to speed up debugging process.

There are some particularities to 2 of the domains:
      -For BS water-levels,the FES2014 tides are added because tides are lacking in the CMEMS model
      -For ARC water-levels, the ocean product in the CMEMS catalogue (ARCTIC_ANALYSIS_FORECAST_PHYS_002_001_A) and the tide and surge model (ARCTIC_ANALYSISFORECAST_PHY_TIDE_002_015) are added together. Some double-counting is expected.

*Note*: this will access the analysis not the forecast if a date is in the past

- Output: Netcdf files based on the bulleting date of the execution day (t0) containing coastal time-series for the selected product-region (ARC,MED,IBI,BS,BAL,NWS) for 7 days [t0-2 : t0+5] (dimensions Ncoastalpoints x times) 

## Worflow description 

Functions called within main, in this order:

1. motu_download.py: 
	Download fields from CMEMS DU given selected region, timeframe and bulletin date>> CMEMS daily fields to $region/data/*.nc
2. coast_water_level_extract_multiple.py : 
	For the given timeframe [t0-2 : t0+5] (=[tini,tend]), snip fields to prescribed coastal locations and interpolate all variables to common location-times >>CMEMS coastal series to $region/data/tseries_coastal_$bulletindate_$tini_$tend.nc
3. coast_water_level_process.py:
	Read the time-series and add other releveant coastal WL contributions (tide if not present, wave setup), write out in daily files >> TWL coastal series to $region/timeseries/TScoast_$region_b$bulletindate_$tini_$tend.nc

The files under $region/timeseries/ are the coastal TWL forecasts. These are used in ECFAS to trigger the warning and mapping component of the system. 

## Test data and checks

Baselines for tests can be found here: https://nexus.mercator-ocean.fr/repository/moistatics/ECFAS 

### Running the trigger (op_trigger) 
- User guide: The trigger is run for all domain-folders found in the output directory as defined by the configuration file. For ECFAS, it should be run after the workflow (op_workflow) has been run for all regions NWS,IBI,MED,BAL,BS,ARC.

The trigger needs as a minimum the configuration file to run, which is the same as used for the workflow (op_workflow). From this configuration file, only the output directory is retreieved as info for op_trigger.

 The optional arguments are the following:
    -t <%Y%m%d_%H%M%S>: Bulleting date for the forecast data. Default: Forecast update time of execution day (same as in op_workflow, check the details for this function in the README)

- Usage: `op_trigger -c <config_file> [-t <%Y%m%d_%H%M%S>]`

Example call: `op_trigger -c ecfas.cnf -t 20220125_000000`

- Output: csv file (trigger/Trigg_info.csv) with all relevant information for coastal flood triggering at the prescribed target coastal points


## Trigger description 
Functions called within main, in this order:

1. coast_water_level_trigger.py : 
	For the coastal TWLs produced in op_workflow, collect all regional coastal series and produce trigger information in the form of a csv file.
  - input files: pre-defined csv files inside ecfas/thresholds/ containing the target coastal locations and thresholds for triggering and duration. 
  - output files: $outdir/trigger/Trigg_info.csv.  Csv file containing for each target coastal point the following information: $outdir corresponds to the parent directory containing all output generated in op_workflow (and prescribed in the configuration file)

    •	Lon : hindcast longitude
    •	Lat : hindcast latitude
    •	lon_map : forecast longitude
    •	lat_map : forecast latitude
    •	map_id: forecast coastal station name 
    •	dist: distance between hindcast and assigned forecast point
    •	thr1: triggering threshold
    •	thr2: duration threshold
    •	flag: triggered YES/NO
    •	fhours: number of hourly points exceeding the duration threshold
    •	maxwl: maximum WL over the forecast
    •	maxwlt: time of max WL
    •	ffirst: first value above triggering threshold 

### Quality checks:

1. Verification of workflow output (op_workflow) against baseline data: 

```
qual_checks [-h] -o <output_dir> -b <baseline_dir> -r <region> -t <YYmmdd_HHMMSS>

Process input arguments:
  -o <output_dir>, --outputs <output_dir>
                        Absolute path to output data to be checked
  -b <baseline_dir>, --baselines <baseline_dir>
                        Absolute path to baseline data to be checked against

optional arguments:
  -h, --help            show this help message and exit

  -r <region>, --region <region>
                        Region of interest, one of ARC, BAL, BS. IBI, MED, NWS. Defaults to all
  -t <YYmmdd_HHMMSS>, --t0 <YYmmdd_HHMMSS>
                        Start time t0 in the format YYmmdd_HHMMSS
```

2. Verification of trigger output (op_trigger) against baseline data: 
```
check_trigger [-h] -o <output_dir> -b <baseline_dir>
Process input arguments.
  -o <output_dir>, --outputs <output_dir>
                        Absolute path to output data to be checked
  -b <baseline_dir>, --baselines <baseline_dir>
                        Absolute path to baseline data to be checked against
optional arguments:
  -h, --help            show this help message and exit
```
3. Validation of the netcdf time-series resulting from the workflow (op_workflow)

```
op_validate [-h] -o <output_dir> -r <region> [-s <Y-m-d H-M-S>] [-e <Y-m-d H-M-S>]

Process input arguments.

optional arguments:
  -h, --help            show this help message and exit
  -o <output_dir>, --outputs <output_dir>
                        Absolute path to output data to be checked
  -r <region>, --region <region>
                        Region of interest, one of ARC, BAL, BS. IBI, MED, NWS, GLO. Defaults to all
  -s <Y-m-d H-M-S>, --t-start <Y-m-d H-M-S>
                        Start time in the format Y-m-d H-M-S
  -e <Y-m-d H-M-S>, --t-end <Y-m-d H-M-S>
                        End time in the format Y-m-d H-M-S
```

### Running unit and functional tests

Unit and functional tests are found in the test and functional_test directories respectively

To run the unit and functional tests pip install pytest, py-cov. Then - for example - run

`pytest -v -s --log-cli-level=INFO test/*`
