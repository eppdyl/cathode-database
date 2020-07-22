# Cathode data
This repository contains the dimensions and digitized data of hollow cathodes.

Orifice hollow cathodes currently considered:
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


Possibly:
- SITAEL (missing dimensions)

    - HC1
    - HC3
    - HC20
    - HC60

The original material (i.e. csv files) is in the folder ''original-material''. 
Each subfolder has a title, and a README for the paper of origin. The name of the folder is author-publication-year.

Multiple papers are merged to get the overall data for a single cathode.
The merged data is stored under the folder institution/cathode/data.csv

## Assembling the database
The database is assembled with the scripts in the folder ''assemble_data''. 
It creates a portable .hdf5 that can be loaded straight into the Python Pandas library. 
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

## LICENSE
The software, CSV files, and database are all licensed under the MIT license.

## CITATION
Please cite the repository if you are using any data from the database.

## CONTRIBUTE
As of June 2020, the database has over 400 data entries with discharge currents
ranging from 1 to 307 A, mass flow rates from 1 sccm to 200 sccm, and 
mercury, xenon, and argon propellants. 

More data is always welcome! 
You can send me data or (preferably) create a pull request to push more data to the database.

Pierre-Yves Taunay, 2020
