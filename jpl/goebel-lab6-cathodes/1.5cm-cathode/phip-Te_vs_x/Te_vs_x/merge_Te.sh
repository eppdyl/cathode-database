#!/bin/bash

for Id in 50 100; do
	FILE='Te_vs_x_Id-'$Id'A_mdot8-12sccm_1.5cm-cathode.csv' 

	cat $FILE | awk '/Curve4/{flag=1;next}/Curve5/{flag=0}flag' | sed '/^$/d' | awk -F',' '{print "\""$1"\",\""$2"\""}' | awk -f transpose.awk | sed 's/^/[/; s/$/],/' | sed -e ':a' -e 'N' -e '$!ba' -e 's/\n/ /g' | sed 's/,$//' | sed "s/^/$Id,8,/"
	cat $FILE | awk '/Curve5/{flag=1;next}/Curve6/{flag=0}flag' | sed '/^$/d' | awk -F',' '{print "\""$1"\",\""$2"\""}'  | awk -f transpose.awk | sed 's/^/[/; s/$/],/' | sed -e ':a' -e 'N' -e '$!ba' -e 's/\n/ /g' | sed 's/,$//' | sed "s/^/$Id,10,/"
	cat $FILE | awk '/Curve6/{flag=1;next}/Curve7/{flag=0}flag' | sed '/^$/d' | awk -F',' '{print "\""$1"\",\""$2"\""}'  | awk -f transpose.awk | sed 's/^/[/; s/$/],/' | sed -e ':a' -e 'N' -e '$!ba' -e 's/\n/ /g' | sed 's/,$//' | sed "s/^/$Id,10,/"
	cat $FILE | awk '/Curve7/{flag=1;next}/Curve8/{flag=0}flag' | sed '/^$/d' | awk -F',' '{print "\""$1"\",\""$2"\""}'  | awk -f transpose.awk | sed 's/^/[/; s/$/],/' | sed -e ':a' -e 'N' -e '$!ba' -e 's/\n/ /g' | sed 's/,$//' | sed "s/^/$Id,10,/"
	cat $FILE | awk '/Curve8/,!/./' | sed '/^$/d; /Curve8/d' | awk -F',' '{print "\""$1"\",\""$2"\""}'  | awk -f transpose.awk | sed 's/^/[/; s/$/],/' | sed -e ':a' -e 'N' -e '$!ba' -e 's/\n/ /g' | sed 's/,$//'| sed "s/^/$Id,12,/"

done

