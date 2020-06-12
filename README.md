# Cathode data
This repository contains the dimensions and digitized data of hollow cathodes.

Orifice hollow cathodes currently considered:
- JPL

    - NSTAR
    - NEXIS
    - LaB6 cathodes

- Lewis

    - Siegfried and Wilbur Hg, Ar, and Xe cathodes 
    - Salhi's Ar and Xe cathode
    - Friedly's Xe cathode

- PEPL

    - Domonkos's Xe cathode

- RAE

    - T6 cathode 

- Princeton

    - PLHC cathode


Possibly:
- SITAEL (missing dimensions)

    - HC1
    - HC3
    - HC20
    - HC60

The original material (i.e. plots, digitizer, csv files) is in the folder ''original-material''. 
Each subfolder has a title, and a README for the paper of origin. The name of the folder is author-publication-year.

Multiple papers are merged to get the overall data for a single cathode.
The merged data is stored under the folder institution/cathode/data.csv

## Assembling the database
The database is assembled with the scripts in the folder ''assemble_data''. 
It creates a portable .hdf5 that can be loaded straight into Pandas. 

## CONTRIBUTE
As of June 2020, the database has over 400 data points with discharge currents
ranging from 1 to 307 A, mass flow rates from 1 sccm to 200 sccm, and 
mercury, xenon, and argon propellants. 

However, more data is always welcome! 
You can send me data or (preferably) create a pull request to push more data
to the database.

Pierre-Yves Taunay, 2020
