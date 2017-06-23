#!/bin/bash

cat P_vs_Id_mdot-5.5sccm.csv | tail -n +2 | awk -F',' '{print $1",5.5,"$2}' >> P_vs_Id-mdot.csv
cat P_vs_mdot_Id-22A.csv | tail -n +2 | awk -F',' '{print "22.0,"$1","$2}' >> P_vs_Id-mdot.csv
