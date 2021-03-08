[![DOI](https://zenodo.org/badge/95235124.svg)](https://zenodo.org/badge/latestdoi/95235124)
# Cathode data
This repository contains the dimensions and digitized data of orified, thermionic hollow cathodes.

The orificed hollow cathodes currently considered are:
- JPL

    - NSTAR
    - NEXIS
    - LaB6 cathodes

- NASA Lewis

    - Siegfried and Wilbur Hg, Ar, and Xe cathodes 
    - Salhi's Ar and Xe cathode
    - Friedly's Xe cathode

- PEPL at University of Michigan

    - Domonkos's Xe cathode

- RAE

    - T6 cathode 

- EPPDyL at Princeton University

    - PLHC cathode

The original material (i.e. csv files) is in the folder ''original-material''. 
Each subfolder has a title, and a README for the paper of origin. The name of the folder is author-publication-year.

Multiple papers are merged to get the overall data for a single cathode.
The merged data is stored under the folder institution/cathode/data.csv

## Assembling the database
The database is assembled with the scripts in the folder ''assemble_data''. 
It creates a portable HDF5 file that can be loaded straight into a Pandas dataframe. 
Default usage:
```bash
python3 make_hdf5_database.py 
```
The script comes with four flags:
- -pe: calculate the total pressure with an empirical correlation if the total pressure is *not* specified (implies "derived quantities")
- -pp: calculate the Pi products for the empirical analysis of the total pressure in hollow cathodes
- -d: calculate the derived quantities (e.g. Reynolds number, Knudsen number, etc.)
- -f: the filename in which to store the file

The flags "-pp" and "-pe" are mutually exclusive.
Note that you *have* to use Pandas to read the data file once it is saved to disk.

## Data currently considered
The data considered at this point is the total pressure, axial electron density, electron temperature, and potential. 
The scripts that are scattered throughout the repository can be easily adapted to include other data, such as the
voltage-current characteristic.

The database columns are defined in the file ''database_columns.csv''.

## LICENSE
* The software (.py, .pynb, .m, .sh) are licensed under the MIT license. See `LICENSE-MIT` for details.
* The data (.csv, .mat, .pkl) are licensed under the CC-BY-4.0 license. See `LICENSE-CC-BY` for details.

## CITATION
Please cite our conference paper if you are using the database and/or repository:
P-Y C R Taunay, C J Wordingham, and E Y Choueiri, "Open electric propulsion with an application to 
thermionic orificed hollow cathodes," AIAA Propulsion and Energy Forum, 2020. AIAA-2020-3638
```
@inproceedings{Taunay2020,
    author = {Taunay, Pierre-Yves C. R. and Wordingham, Christopher J. and Choueiri, Edgar Y.},
    booktitle= {AIAA Propulsion and Energy Forum},
    doi= {10.2514/6.2020-3638},
    note= {AIAA-2020-3638},
    title= {Open Electric Propulsion with an Application to Thermionic Orificed Hollow Cathodes},
    year= {2020}
}
```

## CONTRIBUTE
As of June 2020, the database has over 400 data entries with discharge currents
ranging from 1 to 307 A, mass flow rates from 1 sccm to 200 sccm, and 
mercury, xenon, and argon propellants. 

More data is always welcome! 
You can send me data or create a pull request to push more data to the database.

Pierre-Yves Taunay, 2021
