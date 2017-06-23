#!/bin/bash

for Id in 50 100; do
	FILE='phip_vs_x_Id-'$Id'A_mdot8-12sccm_1.5cm-cathode.csv'

	cat $FILE | awk '/Curve1/{flag=1;next}/Curve2/{flag=0}flag' | sed '/^$/d' | awk -F',' '{print "\""$1"\",\""$2"\""}'  | awk -f transpose.awk | sed 's/^/[/; s/$/],/' | sed -e ':a' -e 'N' -e '$!ba' -e 's/\n/ /g' | sed 's/,$//' | sed "s/^/$Id,8,/"
	SCCM10=`cat $FILE | awk '/Curve2/{flag=1;next}/Curve3/{flag=0}flag' | sed '/^$/d' | awk -F',' '{print "\""$1"\",\""$2"\""}'  | awk -f transpose.awk | sed 's/^/[/; s/$/],/' | sed -e ':a' -e 'N' -e '$!ba' -e 's/\n/ /g' | sed 's/,$//' | sed "s/^/$Id,10,/"`
    ERRM=`cat $FILE | awk '/Curve3/{flag=1;next}/Curve4/{flag=0}flag' | sed '/^$/d' | awk -F',' '{print "\""$2"\""}'  | awk -f transpose.awk | sed 's/^/[/; s/$/],/' | sed -e ':a' -e 'N' -e '$!ba' -e 's/\n/ /g'  | sed 's/,$//'` #| sed "s/^/$Id,10,/"
	ERRP=`cat $FILE | awk '/Curve4/{flag=1;next}/Curve5/{flag=0}flag' | sed '/^$/d' | awk -F',' '{print "\""$2"\""}'  | awk -f transpose.awk | sed 's/^/[/; s/$/],/' | sed -e ':a' -e 'N' -e '$!ba' -e 's/\n/ /g' | sed 's/,$//'` #| sed "s/^/$Id,10,/"
    echo $SCCM10,$ERRM,$ERRP
	cat $FILE | awk '/Curve5/,!/./' | sed '/^$/d; /Curve5/d' | awk -F',' '{print "\""$1"\",\""$2"\""}'  | awk -f transpose.awk | sed 's/^/[/; s/$/],/' | sed -e ':a' -e 'N' -e '$!ba' -e 's/\n/ /g' | sed 's/,$//'| sed "s/^/$Id,12,/"


done

Id=25
FILE='phip_vs_x_Id-'$Id'A_mdot-7sccm_1.5cm-cathode.csv'
cat $FILE | awk '/Curve1/,!/./' | sed '/^$/d; /Curve1/d' | awk -F',' '{print "\""$1"\",\""$2"\""}'  | awk -f transpose.awk | sed 's/^/[/; s/$/],/' | sed -e ':a' -e 'N' -e '$!ba' -e 's/\n/ /g' | sed 's/,$//'| sed "s/^/$Id,7,/"
